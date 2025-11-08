from uuid import UUID, uuid4

from fastembed import LateInteractionTextEmbedding, TextEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    Document,
    FieldCondition,
    Filter,
    HnswConfigDiff,
    MatchValue,
    MultiVectorComparator,
    MultiVectorConfig,
    PointStruct,
    VectorParams,
)

from src.core.controller.base import BaseController
from src.core.logger import logger
from src.models.models import Candidate, File, KnowledgeBaseDocument, User
from src.utils.resume_parser import CandidateExperience

from .repository import CandidateRepository


class CandidateController(BaseController[Candidate]):
    def __init__(
        self, repository: CandidateRepository, vector_db: QdrantClient
    ) -> None:
        super().__init__(model=Candidate, repository=repository)
        self.repository = repository
        self.vector_db = vector_db
        self.colbert_embedding_model = LateInteractionTextEmbedding(
            "colbert-ir/colbertv2.0"
        )
        self.dense_embedding_model = TextEmbedding("BAAI/bge-small-en")

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
        return f"{user.first_name}_candidate_{user.id.hex}"

    def _initialize_vector_collection(self, collection_name: str):
        does_exists = self.vector_db.collection_exists(collection_name)

        if does_exists:
            logger.debug(f"Collection '{collection_name}' already exists")
        else:
            logger.debug(f"Collection '{collection_name}' does not exists.")

            self.vector_db.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=384,
                        distance=Distance.COSINE,
                    ),
                    "colbert": VectorParams(
                        size=128,
                        distance=Distance.COSINE,
                        multivector_config=MultiVectorConfig(
                            comparator=MultiVectorComparator.MAX_SIM
                        ),
                        hnsw_config=HnswConfigDiff(m=0),
                    ),
                },
            )

    def _get_count_of_points_from_collection(
        self, candidate_id: str, collection_name: str
    ):
        self._initialize_vector_collection(collection_name)

        results = self.vector_db.count(
            collection_name=collection_name,
            count_filter=Filter(
                must=[
                    FieldCondition(
                        key="candidate_id",
                        match=MatchValue(value=candidate_id),
                    )
                ]
            ),
        )

        logger.debug(
            f'Found {results} points for collection: "{collection_name}" for candidate: {candidate_id}'
        )

        return results.count

    def _remove_file_from_vector_db(self, candidate_id: str, collection_name: str):
        count = self._get_count_of_points_from_collection(candidate_id, collection_name)

        if count == 0:
            logger.debug(f"No points found for candidate: {candidate_id}")
            return

        result = self.vector_db.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="candidate_id",
                        match=MatchValue(value=candidate_id),
                    )
                ]
            ),
        )

        logger.debug(
            f'Removed points for collection: "{collection_name}" for document: {candidate_id}, with status: "{result.status}"'
        )

        return result.status

    def ingest_candidate(self, candidate_id: UUID, user: User):
        collection_name = self._get_collection_name(user)
        self._initialize_vector_collection(collection_name)

        candidate = self.repository.get_by_id(candidate_id)

        experiences = [CandidateExperience(**exp) for exp in candidate.experiences]

        candidate_text = (
            f"{candidate.name}\n"
            f"{candidate.email}\n"
            f"{candidate.contact}\n"
            f"{candidate.years_of_experience} years of experience\n"
            f"{', '.join(candidate.skills)}\n"
            f"{', '.join(candidate.certifications)}\n"
            f"{'\n'.join(self._get_experience_texts(experiences))}\n"
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=384,
            chunk_overlap=0,
        )
        texts = text_splitter.split_text(candidate_text)

        dense_documents = [
            Document(text=doc, model="BAAI/bge-small-en") for doc in texts
        ]
        colbert_documents = [
            Document(text=doc, model="colbert-ir/colbertv2.0") for doc in texts
        ]

        # for _, colbert in enumerate(colbert_embeddings):
        self.vector_db.upload_points(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=uuid4().hex,
                    payload={"candidate_id": candidate.id.hex, "text": texts[i]},
                    vector={
                        "dense": dense_documents[i],
                        "colbert": colbert_documents[i],
                    },  # type: ignore
                )
                for i in range(len(texts))
            ],
            batch_size=8,
        )

    @staticmethod
    def _get_experience_texts(experiences: list[CandidateExperience]):
        texts = []

        for experience in experiences:
            text = (
                f"{experience.role}\n"
                f"{experience.company}\n"
                f"{experience.start_date.isoformat()} - {experience.end_data.isoformat() if experience.end_data else 'N/A'}\n"
                f"{experience.months_in_experience} months experience\n"
                f"{experience.additional_info}"
            )

            texts.append(text)

        return texts
