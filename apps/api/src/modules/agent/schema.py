from typing import Any, Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class AgentWorkflowResponse(SQLModel):
    mermaid: str
    state: dict[str, list[dict[str, Any]]]


class AgentChatRequest(SQLModel):
    message: str = Field(min_length=1)
    conversation_id: Optional[UUID] = None
