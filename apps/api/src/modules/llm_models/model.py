from typing import Optional

from src.core.config import settings

from .azure_openai import llm as azure_openai
from .deepseek import llm as deepseek
from .open_ai import llm as openai
from .types import LlmModelName


class LlmModelFactory:
    def __init__(self) -> None:
        pass

    def get_model(self, model_name: Optional[LlmModelName] = settings.DEFAULT_LLM):
        match model_name:
            case "deepseek-r1":
                return deepseek
            case "gpt-4o":
                return openai
            case "azure-gpt-4o":
                return azure_openai
            case _:
                return deepseek
