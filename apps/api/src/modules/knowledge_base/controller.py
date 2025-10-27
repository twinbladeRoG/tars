from uuid import UUID

from qdrant_client import QdrantClient

from src.celery.tasks import app as celery_app
from src.celery.tasks import parse_document
from src.celery.utils import get_celery_task_status
from src.modules.file_storage.controller import FileController


class KnowledgeBaseController:
    def __init__(
        self, vector_db: QdrantClient, file_controller: FileController
    ) -> None:
        self.vector_db = vector_db
        self.celery = celery_app
        self.file_controller = file_controller

    def enqueue_document(self, *, file_id: UUID, user_id: UUID):
        document = self.file_controller.get_file_by_id(file_id, user_id)
        task = parse_document.delay(document.filename)  # type: ignore
        result = get_celery_task_status(task.id)
        return result

    def get_task_status(self, id: str):
        result = get_celery_task_status(id)
        return result
