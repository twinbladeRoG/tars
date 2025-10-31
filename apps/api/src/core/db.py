from sqlalchemy import create_engine

from src.core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=settings.SHOW_DB_LOGS
)
