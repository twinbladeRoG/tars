from uuid import UUID

from sqlmodel import SQLModel


class DocumentExtractionRequest(SQLModel):
    file_id: UUID
