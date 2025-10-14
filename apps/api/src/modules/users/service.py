from sqlmodel import Session, select

from src.core.logger import logger
from src.models.models import User


class UserService:
    def get_users(self, session: Session):
        statement = select(User)
        users = session.exec(statement).all()
        logger.info(f"Retrieved {len(users)} users from the database.")

        return users
