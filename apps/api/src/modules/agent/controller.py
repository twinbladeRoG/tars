from typing import Optional
from uuid import UUID

from src.models.models import User
from src.modules.candidate.controller import CandidateController
from src.modules.file_storage.controller import FileController
from src.modules.knowledge_base.controller import KnowledgeBaseController

from .agent import RootAgent


class AgentController:
    def __init__(self) -> None:
        self.agent = RootAgent()

    def get_workflow(
        self,
        file_controller: FileController,
        candidate_controller: CandidateController,
        knowledge_base_controller: KnowledgeBaseController,
        user: User,
    ):
        agent = self.agent.compile(
            file_controller=file_controller,
            candidate_controller=candidate_controller,
            knowledge_base_controller=knowledge_base_controller,
            user=user,
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
        knowledge_base_controller: KnowledgeBaseController,
        conversation_id: Optional[UUID] = None,
        candidate_id: Optional[UUID] = None,
    ):
        return self.agent.stream(
            user=user,
            user_message=user_message,
            conversation_id=conversation_id,
            candidate_id=candidate_id,
            file_controller=file_controller,
            candidate_controller=candidate_controller,
            knowledge_base_controller=knowledge_base_controller,
        )
