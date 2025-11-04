from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    VectorParams,
)

from src.core.controller.base import BaseController
from src.core.logger import logger
from src.models.models import Candidate, File, KnowledgeBaseDocument, User

from .repository import CandidateRepository


class CandidateController(BaseController[Candidate]):
    def __init__(
        self, repository: CandidateRepository, vector_db: QdrantClient
    ) -> None:
        super().__init__(model=Candidate, repository=repository)
        self.repository = repository
        self.vector_db = vector_db

    def get_candidates(self, user: User):
        statement = (
            self.repository._query()
            .join(Candidate.knowledge_base_document)  # type: ignore
            .join(KnowledgeBaseDocument.file)  # type: ignore
            .join(File.owner)  # type: ignore
            .where(User.id == user.id)
        )

        candidates = self.repository.session.exec(statement).all()
        return list(candidates)

    @staticmethod
    def _get_collection_name(user: User):
        return f"{user.first_name}_candidates_{user.id.hex}"

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
