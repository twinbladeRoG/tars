from datetime import datetime
from typing import Any

from sqlmodel import SQLModel


class CeleryTaskStatus(SQLModel):
    task_id: str
    state: str
    status: str
    result: Any = None
    retries: int | None = None
    completed_at: datetime | None = None
