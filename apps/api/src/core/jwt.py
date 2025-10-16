from datetime import timedelta
from typing import Any, Optional

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.core.config import settings
from src.core.logger import logger
from src.utils.time import utcnow


class JwtHandler:
    algorithm = "HS256"
    secret_key = settings.SECRET_KEY
    access_token_expiry = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expiry = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def create_access_token(
        subject: str | Any, *, expires_delta: Optional[timedelta] = None
    ) -> str:
        current_time = utcnow()
        if expires_delta is None:
            expires_delta = timedelta(minutes=JwtHandler.access_token_expiry)
        expire = current_time + expires_delta
        to_encode = {"iat": current_time, "exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, JwtHandler.secret_key, algorithm=JwtHandler.algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(
        subject: str | Any, *, expires_delta: Optional[timedelta] = None
    ) -> str:
        current_time = utcnow()
        if expires_delta is None:
            expires_delta = timedelta(minutes=JwtHandler.refresh_token_expiry)
        expire = current_time + expires_delta
        to_encode = {"iat": current_time, "exp": expire, "sub": str(subject)}
        encode_jwt = jwt.encode(
            to_encode, JwtHandler.secret_key, algorithm=JwtHandler.algorithm
        )
        return encode_jwt

    @staticmethod
    def validate_token(token: str):
        try:
            payload = jwt.decode(
                token, JwtHandler.secret_key, algorithms=[JwtHandler.algorithm]
            )
            return payload
        except ExpiredSignatureError as e:
            logger.error("Token as expired")
            raise e
        except InvalidTokenError as e:
            logger.error("Token as expired")
            raise e
        except Exception as e:
            logger.error(f"Error has occurred while decoding token.\n{e}")
            raise e
