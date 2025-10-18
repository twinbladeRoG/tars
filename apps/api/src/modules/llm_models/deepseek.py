from langchain_deepseek import ChatDeepSeek

from src.core.config import settings

llm = ChatDeepSeek(
    api_base=f"{settings.LOCAL_LLM_HOST}/v1",
    api_key=settings.LOCAL_LLM_SECRET,
    model="deepseek-coder:latest",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
