from celery.result import AsyncResult

from .schema import CeleryTaskStatus
from .tasks import app


def get_celery_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=app)
    res = task_result._get_task_meta()

    if task_result.successful():
        return CeleryTaskStatus(
            task_id=task_id,
            state=task_result.state,
            status=task_result.status,
            result=task_result.result,
            retries=task_result.retries,
            completed_at=task_result.date_done,
        )

    if task_result.failed():
        return CeleryTaskStatus(
            task_id=task_id,
            state=task_result.state,
            status=task_result.status,
            result=str(task_result.result),
            retries=task_result.retries,
            completed_at=task_result.date_done,
        )

    return CeleryTaskStatus(
        task_id=task_id,
        state=task_result.state,
        status=task_result.status,
        result=task_result.result,
        retries=task_result.retries,
        completed_at=task_result.date_done,
    )
