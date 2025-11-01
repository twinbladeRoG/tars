from uuid import UUID

from langchain_core.runnables import RunnableConfig

from src.core.exception import NotFoundException
from src.modules.file_storage.controller import FileController

from ..state import AgentState


class CitationNode:
    def __init__(self, file_controller: FileController) -> None:
        self.file_controller = file_controller

    def __call__(self, state: AgentState, config: RunnableConfig):
        metadata = config.get("metadata", {})
        user_id: str | None = metadata.get("user_id", None)

        results = state["retrieved_points"]
        document_ids = set([])

        if not user_id:
            raise NotFoundException("User not found")

        if results is not None:
            for point in results:
                if point.payload:
                    document_ids.add(UUID(point.payload["file_id"]))

        files = self.file_controller.get_files_by_ids(
            ids=list(document_ids),
            user_id=UUID(user_id),
        )

        return {"citations": files}
