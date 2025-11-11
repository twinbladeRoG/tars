from openai import AzureOpenAI, OpenAI
from openai.types import CreateEmbeddingResponse

from src.core.config import settings

from .types import EmbeddingProvider

llama_cpp = OpenAI(
    base_url=f"{settings.EMBEDDING_MODEL_HOST}/v1",
    api_key=str(settings.EMBEDDING_MODEL_SECRET),
)

openai = OpenAI(api_key=settings.OPEN_API_KEY.get_secret_value())

azure_openai = AzureOpenAI(
    api_key=settings.AZURE_OPEN_AI_KEY.get_secret_value(),
    azure_endpoint=settings.AZURE_OPEN_AI_ENDPOINT,
    api_version=settings.AZURE_OPEN_AI_VERSION,
)


def create_embedding(
    input: str | list[str],
    provider: EmbeddingProvider = settings.DEFAULT_EMBEDDING_MODEL,
) -> CreateEmbeddingResponse:
    match provider:
        case "azure-openai":
            return azure_openai.embeddings.create(
                input=input,
                model="text-embedding-3-large",
                encoding_format="float",
            )
        case "openai":
            return openai.embeddings.create(
                input=input,
                model="text-embedding-3-large",
                encoding_format="float",
            )
        case _:
            return llama_cpp.embeddings.create(
                input=input,
                model=settings.EMBEDDING_MODEL_NAME,
                encoding_format="float",
            )


def get_embedding_size(
    provider: EmbeddingProvider = settings.DEFAULT_EMBEDDING_MODEL,
) -> int:
    match provider:
        case "azure-openai":
            return 3072
        case "openai":
            return 3072
        case _:
            return 1024
