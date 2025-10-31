from uuid import UUID

from src.core.exception import NotFoundException
from src.core.repository.base import BaseRepository
from src.models.models import KnowledgeBaseDocument


class KnowledgeBaseDocumentRepository(BaseRepository[KnowledgeBaseDocument]):
    def upsert_by_file(self, file_id: UUID) -> KnowledgeBaseDocument:
        try:
            return self.get_by("file_id", file_id, unique=True)
        except NotFoundException:
            return self.create({"file_id": file_id})

    def get_by_file_id(self, file_id: UUID) -> KnowledgeBaseDocument:
        return self.get_by("file_id", file_id, unique=True)

    def get_by_task_id(self, task_id: UUID | str) -> KnowledgeBaseDocument | None:
        try:
            return self.get_by("task_id", task_id, unique=True)
        except Exception:
            return None
