from celery.result import AsyncResult

from .schema import CeleryTaskStatus
from .tasks import app


def get_celery_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=app)

    result = CeleryTaskStatus(
        task_id=task_id,
        state=task_result.state,
        status=task_result.status,
        result=task_result.result,
        retries=task_result.retries,
        completed_at=task_result.date_done,
    )

    return result
