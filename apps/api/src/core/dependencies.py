from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .config import Settings
from .db import engine


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_database_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_database_session)]
