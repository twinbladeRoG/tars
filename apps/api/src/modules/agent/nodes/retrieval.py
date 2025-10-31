from langchain_core.runnables import RunnableConfig

from src.core.logger import logger
from src.core.vector_db import vector_db_client
from src.modules.llm_models.embedding import create_embedding

from ..state import AgentState


class RetrievalNode:
    def __init__(self):
        self.vector_db = vector_db_client
        self.create_embedding = create_embedding

    def __call__(self, state: AgentState, config: RunnableConfig):
        metadata = config.get("metadata", {})
        collection_name: str | None = metadata.get("collection_name", None)

        if not collection_name:
            raise Exception("No vector collection found for this user")

        query = state["messages"][-1].content
        query_embedding = self.create_embedding(input=str(query))

        results = self.vector_db.search(
            collection_name=collection_name,
            query_vector=query_embedding.data[0].embedding,
            limit=10,
        )

        logger.debug(
            f"Search results retrieved from vector store is {len(results)} for query: {query}"
        )

        return {"retrieved_points": results}
