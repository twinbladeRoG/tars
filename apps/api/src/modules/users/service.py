from sqlmodel import Session, select

from src.modules.models import User


class UserService:
    def get_users(self, session: Session):
        statement = select(User)
        users = session.exec(statement).all()
        return users
