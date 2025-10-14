from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from src.models.mixins import BaseModelMixin


class UserBase(SQLModel):
    username: str = Field(unique=True, min_items=1, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserPublic(BaseModelMixin, UserBase):
    pass
