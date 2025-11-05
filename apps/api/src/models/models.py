from typing import Optional
from uuid import UUID

from pydantic import field_validator
from sqlmodel import Field, Relationship

from src.core.security import PasswordHandler
from src.modules.candidate.schema import CandidateBase
from src.modules.file_storage.schema import FileBase
from src.modules.knowledge_base.schema import KnowledgeBaseDocumentBase
from src.modules.users.schema import UserBase

from .mixins import BaseModelMixin


class User(BaseModelMixin, UserBase, table=True):
    password: str

    @field_validator("password", mode="after")
    @classmethod
    def generate_hashed_password(cls, value: str) -> str:
        return PasswordHandler.get_password_hash(password=value)

    def __repr__(self) -> str:
        return f"{self.id}: {self.username}, {self.email}"

    files: list["File"] = Relationship(back_populates="owner")


class File(BaseModelMixin, FileBase, table=True):
    owner_id: UUID = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="files")

    knowledge_base_document: Optional["KnowledgeBaseDocument"] = Relationship(
        back_populates="file"
    )


class KnowledgeBaseDocument(BaseModelMixin, KnowledgeBaseDocumentBase, table=True):
    file_id: UUID = Field(foreign_key="file.id", nullable=False, unique=True)
    file: File = Relationship(back_populates="knowledge_base_document")

    candidate: Optional["Candidate"] = Relationship(
        back_populates="knowledge_base_document", cascade_delete=True
    )


class KnowledgeBaseDocumentWithFile(BaseModelMixin, KnowledgeBaseDocumentBase):
    file: File


class Candidate(BaseModelMixin, CandidateBase, table=True):
    knowledge_base_document_id: UUID = Field(
        foreign_key="knowledgebasedocument.id",
        nullable=False,
        unique=True,
        ondelete="CASCADE",
    )
    knowledge_base_document: KnowledgeBaseDocument = Relationship(
        back_populates="candidate"
    )


class CandidateWithKnowledgeBase(BaseModelMixin, KnowledgeBaseDocumentBase):
    knowledge_base_document_id: UUID
    knowledge_base_document: KnowledgeBaseDocument


class CandidateWithScore(BaseModelMixin, CandidateBase):
    score: float
    knowledge_base_document_id: UUID
