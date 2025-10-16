from pydantic import field_validator

from src.core.security import PasswordHandler
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
