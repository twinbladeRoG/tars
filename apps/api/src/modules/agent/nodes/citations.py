from uuid import UUID

from langchain_core.runnables import RunnableConfig

from src.core.exception import NotFoundException
from src.core.logger import logger
from src.models.models import Candidate, CandidateWithScore
from src.modules.candidate.controller import CandidateController
from src.modules.file_storage.controller import FileController

from ..state import AgentState


class CitationNode:
    def __init__(
        self, file_controller: FileController, candidate_controller: CandidateController
    ) -> None:
        self.file_controller = file_controller
        self.candidate_controller = candidate_controller

    def __call__(self, state: AgentState, config: RunnableConfig):
        metadata = config.get("metadata", {})
        user_id: str | None = metadata.get("user_id", None)

        retrieved_points = state["retrieved_points"]
        candidate_retrieved_points = state["candidate_retrieved_points"]
        document_ids = set([])
        knowledge_base_ids = set([])

        if not user_id:
            raise NotFoundException("User not found")

        if retrieved_points is not None:
            for point in retrieved_points:
                if point.payload:
                    document_ids.add(UUID(point.payload["file_id"]))
                    knowledge_base_ids.add(
                        UUID(point.payload["knowledge_base_document_id"])
                    )
                    logger.debug(
                        f"{point.payload['knowledge_base_document_id']} point {point.score}"
                    )

        files = self.file_controller.get_files_by_ids(
            ids=list(document_ids),
            user_id=UUID(user_id),
        )

        resume_candidates: list[Candidate] = []
        for doc_id in knowledge_base_ids:
            candidate = self.candidate_controller.repository.get_by_knowledge_base_id(
                doc_id
            )

            if candidate is None:
                continue

            resume_candidates.append(candidate)

        # Retrieve Candidates
        candidate_ids = {}

        if candidate_retrieved_points is not None:
            for point in candidate_retrieved_points:
                if point.payload:
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
                    **candidate.model_dump(), score=candidate_ids[candidate_id]
                )
            )

        logger.debug(f"From Resumes found {len(resume_candidates)} candidates")
        logger.debug(f"From Candidates found {len(candidates)} candidates")

        return {"citations": files, "candidates": candidates}
