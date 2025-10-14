from typing import Generic, Type, TypeVar
from uuid import UUID

from sqlmodel import Session, select

from src.models.mixins import BaseModelMixin

ModelType = TypeVar("ModelType", bound=BaseModelMixin)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session) -> None:
        self.session = session
        self.model_class: Type[ModelType] = model

    def find_by_id(self, id: UUID) -> ModelType | None:
        statement = select(self.model_class).where(self.model_class.id == id)
        result = self.session.exec(statement).first()
        return result

    def find_all(self):
        statement = select(self.model_class)
        results = self.session.exec(statement).all()
        return results
