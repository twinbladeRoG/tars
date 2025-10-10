from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from src.core.dependencies import SettingsDep

ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str | Any, expires_delta: timedelta, settings: SettingsDep
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"iat": datetime.now(timezone.utc), "exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: str | Any, expires_delta: timedelta, settings: SettingsDep
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"iat": datetime.now(timezone.utc), "exp": expire, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
