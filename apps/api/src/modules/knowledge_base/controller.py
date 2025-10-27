from qdrant_client import QdrantClient

from celery import states
from src.celery.tasks import app as celery_app
from src.celery.tasks import parse_document
from src.celery.utils import get_celery_task_status
from src.core.controller.base import BaseController
from src.models.models import File, KnowledgeBaseDocument

from .repository import KnowledgeBaseDocumentRepository


class KnowledgeBaseController(BaseController[KnowledgeBaseDocument]):
    def __init__(
        self,
        repository: KnowledgeBaseDocumentRepository,
        vector_db: QdrantClient,
    ) -> None:
        super().__init__(model=KnowledgeBaseDocument, repository=repository)
        self.repository = repository
        self.vector_db = vector_db
        self.celery = celery_app

    def enqueue_document(self, *, document: File):
        knowledge_base_document = self.repository.upsert_by_file(document.id)

        task = parse_document.delay(document.filename)  # type: ignore
        result = get_celery_task_status(task_id=task.id)

        knowledge_base_document = self.repository.update(
            knowledge_base_document.id,
            {"task_id": result.task_id, "status": result.status},
        )
        return knowledge_base_document

    def get_task_status(self, id: str):
        result = get_celery_task_status(id)
        knowledge_base_document = self.repository.get_by_task_id(result.task_id)

        if knowledge_base_document is not None:
            attributes = {"status": result.status}

            if result.status == states.SUCCESS:
                attributes["content"] = result.result

            knowledge_base_document = self.repository.update(
                knowledge_base_document.id, attributes
            )
        return knowledge_base_document
