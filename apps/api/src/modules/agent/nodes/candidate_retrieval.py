from langchain_core.runnables import RunnableConfig
from qdrant_client.models import Document, Prefetch

from src.core.logger import logger
from src.core.vector_db import vector_db_client

from ..state import AgentState


class CandidateRetrievalNode:
    def __init__(self, collection_name: str):
        self.vector_db = vector_db_client
        self.collection_name = collection_name

    def __call__(self, state: AgentState, config: RunnableConfig):
        query = state["messages"][-1].content

        results = self.vector_db.query_points(
            collection_name=self.collection_name,
            prefetch=Prefetch(
                query=Document(text=str(query), model="BAAI/bge-small-en"),
                using="dense",
            ),
            query=Document(text=str(query), model="colbert-ir/colbertv2.0"),
            using="colbert",
            limit=5,
        ).points

        logger.debug(
            f"Candidates retrieved from vector store is {len(results)} for query: {query}"
        )

        return {"candidate_retrieved_points": results}
