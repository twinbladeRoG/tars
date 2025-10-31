from uuid import UUID

from sqlmodel import Field, SQLModel

from src.modules.knowledge_base.schema import KnowledgeBaseDocumentBase


class FileBase(SQLModel):
    filename: str = Field(min_length=1, max_length=255)
    original_filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(min_length=1, max_length=255)
    content_length: int = Field(ge=0)


class FileCreate(FileBase):
    owner_id: UUID


class FilePublic(FileBase):
    owner_id: UUID
    knowledge_base_document: KnowledgeBaseDocumentBase | None
