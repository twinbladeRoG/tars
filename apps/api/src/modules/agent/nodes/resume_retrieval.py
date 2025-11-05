from langchain_core.runnables import RunnableConfig

from src.core.logger import logger
from src.core.vector_db import vector_db_client
from src.modules.llm_models.embedding import create_embedding

from ..state import AgentState


class ResumeRetrievalNode:
    def __init__(self, collection_name: str):
        self.vector_db = vector_db_client
        self.create_embedding = create_embedding
        self.collection_name = collection_name

    def __call__(self, state: AgentState, config: RunnableConfig):
        query = state["messages"][-1].content
        query_embedding = self.create_embedding(input=str(query))

        results = self.vector_db.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.data[0].embedding,
            limit=10,
        )

        logger.debug(
            f"Resumes retrieved from vector store is {len(results)} for query: {query}"
        )

        return {"retrieved_points": results}
