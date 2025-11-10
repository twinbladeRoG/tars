from langchain_core.runnables import RunnableConfig

from ..state import AgentState


class ParallelRetrievalNode:
    def __init__(self) -> None:
        pass

    def __call__(self, state: AgentState, config: RunnableConfig):
        pass
