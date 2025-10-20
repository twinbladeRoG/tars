from qdrant_client import QdrantClient

from src.core.config import settings

vector_db_client = QdrantClient(settings.VECTOR_DB_URL)
