from sqlmodel import select

from src.core.repository.base import BaseRepository
from src.models.models import User


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result
