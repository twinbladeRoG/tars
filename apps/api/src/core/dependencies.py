from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError
from qdrant_client import QdrantClient
from sqlmodel import Session

from src.models.models import User
from src.modules.auth.schema import TokenPayload

from .config import Settings
from .db import engine
from .jwt import JwtHandler
from .vector_db import vector_db_client


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_database_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_database_session)]

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/auth/login")

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = JwtHandler.validate_token(token)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError, ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = session.get(User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_vector_database():
    return vector_db_client


VectorDatabaseDep = Annotated[QdrantClient, Depends(get_vector_database)]
