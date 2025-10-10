import uuid
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Column, DateTime, Field, SQLModel

from src.utils.time import utcnow


class UserBase(SQLModel):
    username: str = Field(unique=True, min_items=1, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=utcnow, nullable=False), default=None
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=utcnow, onupdate=utcnow), default=None
    )
