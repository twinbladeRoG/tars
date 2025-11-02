from uuid import UUID

import pymupdf

from celery import Celery
from src.core.config import settings
from src.core.dependencies import get_database_session
from src.core.vector_db import vector_db_client
from src.models.models import KnowledgeBaseDocument, User
from src.modules.file_storage.controller import FileController
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository

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


@app.task(name="parse_document")
def parse_document(file_uri: str, file_id: UUID):
    file_path = FileController._get_local_file_path(file_name=file_uri)

    if not file_path.exists():
        raise Exception(f"File {file_uri} does not exists")

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

    record = knowledge_base_controller.repository.upsert_by_file(file_id=file_id)
    record = knowledge_base_controller.repository.update(record.id, {"content": result})

    return result


@app.task(name="store_embedding")
def store_embeddings(content: str, file_id: UUID, user_id: UUID):
    user_controller = UserController(
        repository=UserRepository(model=User, session=session)
    )

    user = user_controller.get_by_id(user_id)

    from src.modules.knowledge_base.controller import KnowledgeBaseController
    from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository

    knowledge_base_controller = KnowledgeBaseController(
        repository=KnowledgeBaseDocumentRepository(
            model=KnowledgeBaseDocument, session=session
        ),
        vector_db=vector_db_client,
    )

    document = knowledge_base_controller.get_document_by_file_id(
        user=user, file_id=file_id
    )

    knowledge_base_controller.ingest_documents(user=user, files=[document.file])

    return None
