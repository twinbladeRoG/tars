from typing import Generic, Type, TypeVar
from uuid import UUID

from src.core.exception import NotFoundException
from src.core.repository.base import BaseRepository
from src.models.mixins import BaseModelMixin

ModelType = TypeVar("ModelType", bound=BaseModelMixin)


class BaseController(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], repository: BaseRepository) -> None:
        self.model_class = model
        self.repository = repository

    def get_by_id(self, id: UUID) -> ModelType | None:
        item = self.repository.find_by_id(id)
        if not item:
            raise NotFoundException(
                f"{self.model_class.__name__} with id {id} not found"
            )

        return item
