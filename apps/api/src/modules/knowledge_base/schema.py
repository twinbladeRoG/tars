from sqlmodel import SQLModel


class DocumentExtractionRequest(SQLModel):
    file_name: str
