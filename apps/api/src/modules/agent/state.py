import operator
from typing import Optional

from langchain.messages import AnyMessage
from pydantic import BaseModel
from qdrant_client.models import ScoredPoint
from typing_extensions import Annotated, TypedDict


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    retrieved_points: list[ScoredPoint] | None
    llm_calls: Optional[int]
    citations: Optional[list[BaseModel]]
