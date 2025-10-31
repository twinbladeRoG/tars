import operator

from langchain.messages import AnyMessage
from qdrant_client.models import ScoredPoint
from typing_extensions import Annotated, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    retrieved_points: list[ScoredPoint] | None
    llm_calls: int
