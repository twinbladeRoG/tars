from uuid import UUID

from langchain_core.runnables import RunnableConfig

from src.core.exception import NotFoundException
from src.models.models import Candidate
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

        results = state["retrieved_points"]
        document_ids = set([])
        knowledge_base_ids = set([])

        if not user_id:
            raise NotFoundException("User not found")

        if results is not None:
            for point in results:
                if point.payload:
                    document_ids.add(UUID(point.payload["file_id"]))
                    knowledge_base_ids.add(
                        UUID(point.payload["knowledge_base_document_id"])
                    )

        files = self.file_controller.get_files_by_ids(
            ids=list(document_ids),
            user_id=UUID(user_id),
        )

        candidates: list[Candidate] = []
        for doc_id in knowledge_base_ids:
            candidate = self.candidate_controller.repository.get_by_knowledge_base_id(
                doc_id
            )

            if candidate is None:
                continue

            candidates.append(candidate)

        return {"citations": files, "candidates": candidates}
