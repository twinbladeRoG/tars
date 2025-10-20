from time import sleep

from celery import Celery
from src.core.config import settings

app = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)


@app.task
def parse_document(doc_uri: str):
    sleep(10)
