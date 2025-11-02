from uuid import UUID, uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from celery import chain, states
from src.celery.tasks import app as celery_app
from src.celery.tasks import create_candidate, parse_document, store_embeddings
from src.celery.utils import get_celery_task_status
from src.core.controller.base import BaseController
from src.core.exception import BadRequestException, NotFoundException
from src.core.logger import logger
from src.models.models import File, KnowledgeBaseDocument, User
from src.modules.llm_models.embedding import create_embedding

from .repository import KnowledgeBaseDocumentRepository


class KnowledgeBaseController(BaseController[KnowledgeBaseDocument]):
    def __init__(
        self,
        repository: KnowledgeBaseDocumentRepository,
        vector_db: QdrantClient,
    ) -> None:
        super().__init__(model=KnowledgeBaseDocument, repository=repository)
        self.repository = repository
        self.vector_db = vector_db
        self.celery = celery_app

    def enqueue_document(self, *, user: User, document: File):
        knowledge_base_document = self.repository.upsert_by_file(document.id)

        workflow = chain(
            parse_document.s(document.filename, document.id),  # type: ignore
            store_embeddings.s(document.id, user.id),  # type: ignore
            create_candidate.s(),  # type: ignore
        )
        task = workflow.apply_async()

        result = get_celery_task_status(task_id=task.id)  # type: ignore

        knowledge_base_document = self.repository.update(
            knowledge_base_document.id,
            {"task_id": result.task_id, "status": result.status},
        )
        return knowledge_base_document

    def get_task_status(self, id: str):
        result = get_celery_task_status(id)
        knowledge_base_document = self.repository.get_by_task_id(result.task_id)

        if knowledge_base_document is not None:
            attributes = {"status": result.status}

            if result.status == states.SUCCESS:
                attributes["content"] = result.result

            knowledge_base_document = self.repository.update(
                knowledge_base_document.id, attributes
            )
        return knowledge_base_document

    def _initialize_vector_collection(self, collection_name: str):
        does_exists = self.vector_db.collection_exists(collection_name)

        if does_exists:
            logger.info(f"Collection '{collection_name}' already exists")
        else:
            logger.info(f"Collection '{collection_name}' does not exists.")

            self.vector_db.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )

    @staticmethod
    def _get_collection_name(user: User):
        return f"{user.first_name}_{user.id.hex}"

    def ingest_documents(self, user: User, files: list[File]):
        for doc in files:
            if not doc.knowledge_base_document:
                raise BadRequestException(
                    f"File {doc.original_filename} has not been extracted yet!"
                )

            if not doc.knowledge_base_document.content:
                raise BadRequestException(
                    f"File {doc.original_filename} has not been extracted yet!"
                )

        collection_name = self._get_collection_name(user)
        self._initialize_vector_collection(collection_name)

        for doc in files:
            if doc.knowledge_base_document and doc.knowledge_base_document.content:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=512,
                    chunk_overlap=20,
                )
                texts = text_splitter.split_text(doc.knowledge_base_document.content)
                embeddings = create_embedding(input=texts)
                self._remove_file_from_vector_db(
                    file_id=doc.id.hex,
                    collection_name=collection_name,
                )

                for _, (text, embedding) in enumerate(zip(texts, embeddings.data)):
                    self.vector_db.upload_points(
                        collection_name=collection_name,
                        points=[
                            PointStruct(
                                id=uuid4().hex,
                                vector=embedding.embedding,
                                payload={
                                    "text": text,
                                    "file_id": doc.id.hex,
                                    "knowledge_base_document_id": doc.knowledge_base_document.id.hex,
                                },
                            )
                        ],
                    )

        return files

    def _get_count_of_points_from_collection(self, file_id: str, collection_name: str):
        self._initialize_vector_collection(collection_name)

        results = self.vector_db.count(
            collection_name=collection_name,
            count_filter=Filter(
                must=[
                    FieldCondition(
                        key="file_id",
                        match=MatchValue(value=file_id),
                    )
                ]
            ),
        )

        logger.debug(
            f'Found {results} points for collection: "{collection_name}" for file: {file_id}'
        )

        return results.count

    def _remove_file_from_vector_db(self, file_id: str, collection_name: str):
        count = self._get_count_of_points_from_collection(file_id, collection_name)

        if count == 0:
            logger.debug(f"No points found for document: {file_id}")
            return

        result = self.vector_db.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="file_id",
                        match=MatchValue(value=file_id),
                    )
                ]
            ),
        )

        logger.debug(
            f'Removed points for collection: "{collection_name}" for document: {file_id}, with status: "{result.status}"'
        )

        return result.status

    def get_user_knowledge_base_documents(self, user: User):
        statement = (
            self.repository._query()
            .join(self.model_class.file)  # type: ignore
            .join(File.owner)  # type: ignore
            .where(User.id == user.id)
        )

        results = self.repository.session.exec(statement).all()
        return list(results)

    def remove_knowledge_base_document(self, document_id: UUID, user: User):
        document = self.get_by_id(document_id)
        self._remove_file_from_vector_db(
            file_id=document.file_id.hex,
            collection_name=self._get_collection_name(user),
        )

        self.repository.delete(document)

    def get_document_by_file_id(self, user: User, file_id: UUID):
        doc = self.repository.session.exec(
            self.repository._query()
            .join(self.model_class.file)  # type: ignore
            .join(File.owner)  # type: ignore
            .where(
                self.model_class.file_id == file_id,
                User.id == user.id,
            )
        ).one_or_none()

        if doc is None:
            raise NotFoundException(f"No document exists with file id: {file_id}")

        return doc

    def get_document_by_id(self, id: UUID, user: User):
        doc = self.repository.session.exec(
            self.repository._query()
            .join(self.model_class.file)  # type: ignore
            .join(File.owner)  # type: ignore
            .where(
                self.model_class.id == id,
                User.id == user.id,
            )
        ).one_or_none()

        if doc is None:
            raise NotFoundException(f"No document exists with id: {id}")

        return doc
