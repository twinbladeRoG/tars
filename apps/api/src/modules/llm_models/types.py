from typing import Literal

type EmbeddingProvider = Literal["azure-openai", "openai", "llama-cpp"]

type LlmModelName = Literal["gpt-4o", "deepseek-r1", "azure-gpt-4o"]
