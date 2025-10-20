from fastapi import APIRouter

from src.celery.schema import CeleryTaskStatus
from src.celery.tasks import parse_document
from src.celery.utils import get_celery_task_status

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])


@router.post("/")
def enqueue_document():
    task = parse_document.delay("test")  # type: ignore
    return {"message": "ok", "task_id": task.id}


@router.get("/status/{id}", response_model=CeleryTaskStatus)
def task_status(id: str):
    result = get_celery_task_status(id)

    return result
