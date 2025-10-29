from uuid import UUID

import pymupdf

from celery import Celery
from src.core.config import settings
from src.core.dependencies import get_database_session
from src.core.vector_db import vector_db_client
from src.models.models import KnowledgeBaseDocument
from src.modules.file_storage.controller import FileController

app = Celery(
    __name__,
    broker=settings.REDIS_URL,
    backend=settings.CELERY_BACKEND_URI,
)

app.conf.task_track_started = True
app.conf.result_extended = True
app.conf.database_create_tables_at_setup = True

session_generator = get_database_session()
session = next(session_generator)


@app.task
def parse_document(doc_uri: str, doc_id: UUID):
    file_path = FileController._get_local_file_path(file_name=doc_uri)

    if not file_path.exists():
        raise Exception(f"File {doc_uri} does not exists")

    doc = pymupdf.open(file_path.resolve())

    pages: list[str] = [page.get_text() for page in doc]  # type: ignore
    result = chr(12).join(pages)

    doc.close()

    from src.modules.knowledge_base.controller import KnowledgeBaseController
    from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository

    knowledge_base_controller = KnowledgeBaseController(
        repository=KnowledgeBaseDocumentRepository(
            model=KnowledgeBaseDocument, session=session
        ),
        vector_db=vector_db_client,
    )

    record = knowledge_base_controller.repository.upsert_by_file(file_id=doc_id)
    record = knowledge_base_controller.repository.update(record.id, {"content": result})

    return result
