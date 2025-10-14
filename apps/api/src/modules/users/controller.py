from uuid import UUID

from src.core.controller.base import BaseController
from src.core.repository.base import BaseRepository
from src.models.models import User


class UserController(BaseController[User]):
    def __init__(self, repository: BaseRepository) -> None:
        super().__init__(model=User, repository=repository)
        self.repository = repository

    def get_by_id(self, id: UUID) -> User | None:
        return self.repository.find_by_id(id)
