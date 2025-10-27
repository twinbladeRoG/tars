from fastapi import APIRouter

from src.celery.schema import CeleryTaskStatus
from src.core.dependencies import CurrentUser
from src.core.factory.factory import KnowledgeBaseControllerDeps

from .schema import DocumentExtractionRequest

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])


@router.post("/", response_model=CeleryTaskStatus)
def enqueue_document(
    body: DocumentExtractionRequest,
    knowledge_base_controller: KnowledgeBaseControllerDeps,
    user: CurrentUser,
):
    return knowledge_base_controller.enqueue_document(
        file_id=body.file_id, user_id=user.id
    )


@router.get("/status/{id}", response_model=CeleryTaskStatus)
def task_status(id: str, knowledge_base_controller: KnowledgeBaseControllerDeps):
    return knowledge_base_controller.get_task_status(id)
