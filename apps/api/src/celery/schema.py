from datetime import datetime
from typing import Any

from sqlmodel import SQLModel


class CeleryTaskStatus(SQLModel):
    task_id: str
    state: str
    status: str
    result: Any
    retries: int | None
    completed_at: datetime | None
