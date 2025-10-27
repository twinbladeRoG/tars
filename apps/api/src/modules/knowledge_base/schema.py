from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class DocumentExtractionRequest(SQLModel):
    file_id: UUID


class KnowledgeBaseDocumentBase(SQLModel):
    file_id: UUID
    status: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    task_id: Optional[str] = Field(default=None)
