import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field

from src.utils.time import utcnow


class TimeStampMixin(BaseModel):
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=utcnow, sa_column_kwargs={"onupdate": utcnow}
    )


class BaseModelMixin(TimeStampMixin, BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
