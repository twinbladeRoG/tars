from src.core.controller.base import BaseController
from src.models.models import User

from .repository import UserRepository


class UserController(BaseController[User]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(model=User, repository=repository)
        self.repository = repository
