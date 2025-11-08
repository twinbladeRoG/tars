from fastembed.rerank.cross_encoder import TextCrossEncoder
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
        self.reranker = TextCrossEncoder(
            model_name="jinaai/jina-reranker-v2-base-multilingual"
        )

    def __call__(self, state: AgentState, config: RunnableConfig):
        query = state["messages"][-1].content
        query_embedding = self.create_embedding(input=str(query))

        results = self.vector_db.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.data[0].embedding,
            limit=5,
        )

        logger.debug(
            f"Resumes retrieved from vector store is {len(results)} for query: {query}"
        )

        resume_chunks = []
        for i, hit in enumerate(results):
            resume_chunks.append(hit.payload["text"])  # type: ignore

        new_scores = list(self.reranker.rerank(str(query), resume_chunks))
        ranking = [(i, score) for i, score in enumerate(new_scores)]
        ranking.sort(key=lambda x: x[1], reverse=True)

        sorted_results = [results[idx] for idx, _ in ranking]

        return {"resume_retrieved_points": sorted_results}
