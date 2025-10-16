from typing import Generic, Sequence, Type, TypeVar
from uuid import UUID

from sqlmodel import SQLModel

from src.core.exception import NotFoundException
from src.core.repository.base import BaseRepository
from src.models.mixins import BaseModelMixin

ModelType = TypeVar("ModelType", bound=BaseModelMixin)


class BaseController(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], repository: BaseRepository) -> None:
        self.model_class = model
        self.repository = repository

    def get_by_id(self, id: UUID) -> ModelType:
        response = self.repository.get_by(field="id", value=id, unique=True)

        if not response:
            raise NotFoundException(
                f"{self.model_class.__name__} with id {id} not found"
            )

        return response

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        response = self.repository.get_all(skip=skip, limit=limit)
        return response

    def create(self, create_model: SQLModel) -> ModelType:
        response = self.repository.create(create_model.model_dump())
        return response
