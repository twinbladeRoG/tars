from typing import Dict, Set, Tuple
from uuid import UUID

from langchain_core.runnables import RunnableConfig
from qdrant_client.models import ScoredPoint

from src.core.exception import NotFoundException
from src.core.logger import logger
from src.models.models import CandidateWithResume, CandidateWithScore, File
from src.modules.candidate.controller import CandidateController
from src.modules.file_storage.controller import FileController
from src.modules.knowledge_base.controller import KnowledgeBaseController

from ..state import AgentState


class CitationNode:
    def __init__(
        self,
        file_controller: FileController,
        candidate_controller: CandidateController,
        knowledge_base_controller: KnowledgeBaseController,
    ) -> None:
        self.file_controller = file_controller
        self.candidate_controller = candidate_controller
        self.knowledge_base_controller = knowledge_base_controller

    def __call__(self, state: AgentState, config: RunnableConfig):
        metadata = config.get("metadata", {})
        user_id_hex: str | None = metadata.get("user_id", None)

        if user_id_hex is None:
            raise NotFoundException("User not found")

        user_id = UUID(user_id_hex)

        resume_retrieved_points = state["resume_retrieved_points"]
        candidate_retrieved_points = state["candidate_retrieved_points"]

        if not user_id:
            raise NotFoundException("User not found")

        files, resume_candidates = self._get_resume_candidates(
            user_id, resume_retrieved_points
        )

        candidates = self._get_candidates(candidate_retrieved_points)

        logger.debug(f"From Resumes found {len(resume_candidates)} candidates")
        logger.debug(f"From Candidates found {len(candidates)} candidates")

        return {
            "citations": files,
            "candidates": candidates,
            "resume_candidates": resume_candidates,
        }

    def _get_resume_candidates(
        self, user_id: UUID, resume_retrieved_points: list[ScoredPoint] | None
    ) -> Tuple[list[File], list[CandidateWithResume]]:
        if resume_retrieved_points is None:
            return [], []

        document_ids: Set[UUID] = set([])
        knowledge_base_ids: Dict[str, list[str]] = {}

        for point in resume_retrieved_points:
            if point.payload is None:
                continue

            document_ids.add(UUID(point.payload["file_id"]))

            knowledge_base_id = UUID(point.payload["knowledge_base_document_id"])

            doesExists = knowledge_base_ids.get(knowledge_base_id.hex, None)

            if doesExists is None:
                knowledge_base_ids[knowledge_base_id.hex] = [point.payload["text"]]
            else:
                knowledge_base_ids[knowledge_base_id.hex].append(point.payload["text"])

            logger.debug(
                f"{point.payload['knowledge_base_document_id']} point {point.score}"
            )

        files = self.file_controller.get_files_by_ids(
            ids=list(document_ids),
            user_id=user_id,
        )

        resume_candidates: list[CandidateWithResume] = []

        for doc_id in knowledge_base_ids.keys():
            candidate = self.candidate_controller.repository.get_by_knowledge_base_id(
                UUID(doc_id)
            )
            knowledge_base_document = self.knowledge_base_controller.get_by_id(
                UUID(doc_id)
            )

            if candidate is None:
                continue

            resume_candidates.append(
                CandidateWithResume(
                    **candidate.model_dump(),
                    chunks=knowledge_base_ids[doc_id],
                    knowledge_base_document=knowledge_base_document,
                )
            )

        return files, resume_candidates

    def _get_candidates(self, candidate_retrieved_points: list[ScoredPoint] | None):
        if candidate_retrieved_points is None:
            return []

        candidate_ids: Dict[str, float] = {}

        for point in candidate_retrieved_points:
            if point.payload is None:
                continue

            candidate_id = UUID(point.payload["candidate_id"])
            previous_score = candidate_ids.get(candidate_id.hex, None)

            if previous_score is None:
                candidate_ids[candidate_id.hex] = point.score
            elif point.score > previous_score:
                candidate_ids[candidate_id.hex] = point.score

                logger.debug(f"{candidate_id} point {point.score}")

        candidates: list[CandidateWithScore] = []

        for candidate_id in candidate_ids:
            candidate = self.candidate_controller.get_by_id(UUID(candidate_id))
            candidates.append(
                CandidateWithScore(
                    **candidate.model_dump(),
                    score=candidate_ids[candidate_id],
                )
            )

        return candidates
