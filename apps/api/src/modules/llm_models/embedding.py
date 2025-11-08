from openai import OpenAI
from openai.types import CreateEmbeddingResponse

from src.core.config import settings

openai = OpenAI(
    base_url=f"{settings.EMBEDDING_MODEL_HOST}/v1",
    api_key=str(settings.EMBEDDING_MODEL_SECRET),
)


def create_embedding(input: str | list[str]) -> CreateEmbeddingResponse:
    embeddings = openai.embeddings.create(
        input=input,
        model=settings.EMBEDDING_MODEL_NAME,
        encoding_format="float",
    )
    return embeddings
