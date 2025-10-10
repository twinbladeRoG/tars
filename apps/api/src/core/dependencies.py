from typing import Annotated

from functools import lru_cache
from .config import Settings
from fastapi import Depends


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
