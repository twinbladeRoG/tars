from typing import Literal, Optional

from .deepseek import llm as deepseek
from .open_ai import llm as openai

type LlmModelName = Literal["gpt-4o", "deepseek-r1"]


class LlmModelFactory:
    def __init__(self) -> None:
        pass

    def get_model(self, model_name: Optional[LlmModelName] = "deepseek-r1"):
        match model_name:
            case "deepseek-r1":
                return deepseek
            case "gpt-4o":
                return openai
            case _:
                return deepseek
