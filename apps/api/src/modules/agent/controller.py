from typing import Any, Optional
from uuid import UUID

from src.models.models import User

from .agent import RootAgent


class AgentController:
    def __init__(self) -> None:
        self.agent = RootAgent()

    def __call__(self) -> Any:
        pass

    def get_workflow(self):
        agent = self.agent.compile()
        mermaid = agent.get_graph(xray=True).draw_mermaid()
        state = agent.get_graph(xray=True).to_json()

        return state, mermaid

    def stream(
        self,
        user: User,
        user_message: str,
        conversation_id: Optional[UUID | None] = None,
    ):
        return self.agent.stream(
            user=user, user_message=user_message, conversation_id=conversation_id
        )
