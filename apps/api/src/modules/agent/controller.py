from typing import Optional
from uuid import UUID

from src.models.models import User
from src.modules.candidate.controller import CandidateController
from src.modules.file_storage.controller import FileController

from .agent import RootAgent


class AgentController:
    def __init__(self) -> None:
        self.agent = RootAgent()

    def get_workflow(
        self, file_controller: FileController, candidate_controller: CandidateController
    ):
        agent = self.agent.compile(
            file_controller=file_controller, candidate_controller=candidate_controller
        )
        mermaid = agent.get_graph(xray=True).draw_mermaid()
        state = agent.get_graph(xray=True).to_json()

        return state, mermaid

    def stream(
        self,
        user: User,
        user_message: str,
        *,
        file_controller: FileController,
        candidate_controller: CandidateController,
        conversation_id: Optional[UUID | None] = None,
    ):
        return self.agent.stream(
            user=user,
            user_message=user_message,
            conversation_id=conversation_id,
            file_controller=file_controller,
            candidate_controller=candidate_controller,
        )
