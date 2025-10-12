from sqlalchemy import create_engine

from src.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
