from uuid import UUID

from pydantic import field_validator
from sqlmodel import Field, Relationship

from src.core.security import PasswordHandler
from src.modules.file_storage.schema import FileBase
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
