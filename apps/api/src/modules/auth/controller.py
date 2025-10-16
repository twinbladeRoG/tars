from uuid import UUID

from pydantic import EmailStr

from src.core.controller.base import BaseController
from src.core.exception import NotFoundException
from src.core.jwt import JwtHandler
from src.core.logger import logger
from src.core.security import PasswordHandler
from src.models.models import User
from src.modules.users.repository import UserRepository

from .schema import TokenPayload, Tokens


class AuthController(BaseController[User]):
    def __init__(self, repository: UserRepository) -> None:
        super().__init__(model=User, repository=repository)
        self.repository = repository

    def login(self, email: EmailStr, password: str):
        user = self.repository.get_by_email(email)

        if not user:
            raise NotFoundException(f"Either email or password is wrong")

        if not PasswordHandler.verify_password(password, user.password):
            raise NotFoundException(f"Either email or password is wrong")

        access_token = JwtHandler.create_access_token(user.id)
        refresh_token = JwtHandler.create_refresh_token(user.id)

        tokens = Tokens(access_token=access_token, refresh_token=refresh_token)

        return user, tokens

    def generate_fresh_tokens(self, refresh_token: str):
        try:
            payload = JwtHandler.validate_token(refresh_token)
            token_data = TokenPayload(**payload)
            user = self.get_by_id(UUID(token_data.sub))
            access_token = JwtHandler.create_access_token(user.id)
            tokens = Tokens(access_token=access_token, refresh_token=refresh_token)
            return tokens
        except Exception as e:
            logger.error(e)
            raise e
