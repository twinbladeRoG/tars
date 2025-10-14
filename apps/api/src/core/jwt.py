from datetime import timedelta
from typing import Any

import jwt

from core.config import settings
from src.utils.time import utcnow


class JwtHandler:
    algorithm = "HS256"
    secret_key = settings.SECRET_KEY

    @staticmethod
    def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
        current_time = utcnow()
        expire = current_time + expires_delta
        to_encode = {"iat": current_time, "exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, JwtHandler.secret_key, algorithm=JwtHandler.algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: str | Any, expires_delta: timedelta) -> str:
        current_time = utcnow()
        expire = current_time + expires_delta
        to_encode = {"iat": current_time, "exp": expire, "sub": str(subject)}
        encode_jwt = jwt.encode(
            to_encode, JwtHandler.secret_key, algorithm=JwtHandler.algorithm
        )
        return encode_jwt
