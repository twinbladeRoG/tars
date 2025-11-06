from langchain_openai import AzureChatOpenAI

from src.core.config import settings

llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPEN_AI_ENDPOINT,
    api_key=settings.AZURE_OPEN_AI_KEY,
    api_version=settings.AZURE_OPEN_AI_VERSION,
    model="gpt-4o-mini",
    temperature=0,
    timeout=None,
    max_retries=2,
)
