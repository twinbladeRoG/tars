from typing import Any

from sqlmodel import SQLModel


class AgentWorkflowResponse(SQLModel):
    mermaid: str
    state: dict[str, list[dict[str, Any]]]
