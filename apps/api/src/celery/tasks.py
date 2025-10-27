import pymupdf

from celery import Celery
from src.core.config import settings
from src.modules.file_storage.controller import FileController

app = Celery(
    __name__,
    broker=settings.REDIS_URL,
    backend=settings.CELERY_BACKEND_URI,
)

app.conf.task_track_started = True
app.conf.result_extended = True
app.conf.database_create_tables_at_setup = True


@app.task
def parse_document(doc_uri: str):
    file_path = FileController._get_local_file_path(file_name=doc_uri)

    if not file_path.exists():
        raise Exception(f"File {doc_uri} does not exists")

    doc = pymupdf.open(file_path.resolve())

    pages: list[str] = [page.get_text() for page in doc]  # type: ignore
    result = chr(12).join(pages)

    doc.close()

    return result
