from pydantic import field_validator

from src.core.security import get_password_hash
from src.modules.users.schema import UserCreate

from .mixins import BaseModelMixin


class User(BaseModelMixin, UserCreate, table=True):
    @field_validator("password", mode="after")
    @classmethod
    def generate_hashed_password(cls, value: str) -> str:
        return get_password_hash(password=value)

    def __repr__(self) -> str:
        return f"{self.id}: {self.username}, {self.email}"
