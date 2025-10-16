from src.core.repository.base import BaseRepository
from src.models.models import User


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> User | None:
        response = self.get_by(field="email", value=email, unique=True)
        return response
