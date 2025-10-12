import uuid
from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import Column, DateTime, Field

from src.core.security import get_password_hash
from src.modules.users.schema import UserBase
from src.utils.time import utcnow


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=utcnow, nullable=False), default=None
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=utcnow, onupdate=utcnow), default=None
    )

    password: str = Field(min_length=8, max_length=40)

    @field_validator("password", mode="after")
    @classmethod
    def generate_hashed_password(cls, value: str) -> str:
        return get_password_hash(password=value)

    def __repr__(self) -> str:
        return f"{self.id}: {self.username}, {self.email}"
