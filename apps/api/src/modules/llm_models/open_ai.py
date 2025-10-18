from langchain_openai import ChatOpenAI

from src.core.config import settings

llm = ChatOpenAI(
    api_key=settings.OPEN_API_KEY,
    model="gpt-4o-mini",
    temperature=0,
    timeout=None,
    max_retries=2,
)
