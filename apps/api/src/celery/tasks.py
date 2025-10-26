from pathlib import Path

import pymupdf
import pymupdf4llm

from celery import Celery
from src.core.config import settings

app = Celery(
    __name__,
    broker=settings.REDIS_URL,
    backend=settings.CELERY_BACKEND_URI,
)

DATA_PATH = Path("data")


@app.task
def parse_document(doc_uri: str):
    file_path = DATA_PATH / doc_uri

    if not file_path.exists():
        raise Exception(f"File {doc_uri} does not exists")

    doc = pymupdf.open(file_path.resolve())

    pages: list[str] = [page.get_text() for page in doc]  # type: ignore
    result = chr(12).join(pages)

    doc.close()

    hi = pymupdf4llm.to_markdown(file_path.resolve())

    return result
