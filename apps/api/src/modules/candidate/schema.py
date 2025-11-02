from typing import Dict, List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlmodel import Column, Field, SQLModel


class CandidateBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(min_length=1)
    contact: Optional[str] = Field(default=None, nullable=True)
    years_of_experience: float = Field(default=0)

    skills: List[str] = Field(sa_column=Column(ARRAY(String)))
    experiences: List[Dict[str, str]] = Field(sa_column=Column(JSONB))
    certifications: List[str] = Field(sa_column=Column(ARRAY(String)))


class CandidateCreate(CandidateBase):
    knowledge_base_document_id: UUID
