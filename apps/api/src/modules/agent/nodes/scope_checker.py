from uuid import UUID

from langchain_core.runnables import RunnableConfig

from src.core.logger import logger

from ..state import AgentState


class ScopeCheckerNode:
    def __init__(self) -> None:
        pass

    def __call__(self, state: AgentState, config: RunnableConfig):
        candidate_id = (
            UUID(state["candidate_id"]) if state["candidate_id"] is not None else None
        )

        logger.debug(f"Selected candidate: {candidate_id}")

        if candidate_id is None:
            return False
        else:
            return True
