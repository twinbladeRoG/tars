import json
import traceback
from typing import Optional
from uuid import UUID, uuid4

from langchain.messages import AIMessage, AnyMessage, HumanMessage
from langchain_core.runnables.config import (
    RunnableConfig,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from src.core.logger import logger
from src.models.models import CandidateWithResume, CandidateWithScore, User
from src.modules.candidate.controller import CandidateController
from src.modules.file_storage.controller import FileController
from src.modules.knowledge_base.controller import KnowledgeBaseController

from .nodes.agent import AgentNode
from .nodes.candidate_retrieval import CandidateRetrievalNode
from .nodes.chatbot import ChatBotNode
from .nodes.citations import CitationNode
from .nodes.parallel_retrieval import ParallelRetrievalNode
from .nodes.resume_retrieval import ResumeRetrievalNode
from .nodes.scope_checker import ScopeCheckerNode
from .state import AgentState

memory = MemorySaver()


class RootAgent:
    def __init__(self) -> None:
        self.agent = None
        self.memory = memory

    def compile(
        self,
        *,
        file_controller: FileController,
        candidate_controller: CandidateController,
        knowledge_base_controller: KnowledgeBaseController,
        user: User,
    ):
        if self.agent is not None:
            logger.debug("Agent already complied")
            return self.agent

        agent_builder = StateGraph(AgentState)

        # Add Nodes
        agent_builder.add_node("chatbot", ChatBotNode())
        agent_builder.add_node(
            "resume_retrieval",
            ResumeRetrievalNode(
                collection_name=KnowledgeBaseController._get_collection_name(user)
            ),
        )
        agent_builder.add_node(
            "citations",
            CitationNode(
                file_controller=file_controller,
                candidate_controller=candidate_controller,
                knowledge_base_controller=knowledge_base_controller,
            ),
        )
        agent_builder.add_node(
            "candidate_retrieval",
            CandidateRetrievalNode(
                collection_name=CandidateController._get_collection_name(user)
            ),
        )
        # agent_builder.add_node("scope_checker", ScopeCheckerNode())
        agent_builder.add_node("parallel_retrieval", ParallelRetrievalNode())
        agent_builder.add_node(
            "agent", AgentNode(candidate_controller=candidate_controller)
        )

        # Add Edges
        # agent_builder.add_edge(START, "scope_checker")
        agent_builder.add_conditional_edges(
            START,
            ScopeCheckerNode(),
            {True: "agent", False: "parallel_retrieval"},
        )

        agent_builder.add_edge("parallel_retrieval", "resume_retrieval")
        agent_builder.add_edge("parallel_retrieval", "candidate_retrieval")
        agent_builder.add_edge("resume_retrieval", "citations")
        agent_builder.add_edge("candidate_retrieval", "citations")
        agent_builder.add_edge("citations", "chatbot")
        agent_builder.add_edge("chatbot", END)

        agent_builder.add_edge("agent", END)

        agent = agent_builder.compile(checkpointer=self.memory)
        self.agent = agent
        return agent

    def stream(
        self,
        *,
        user: User,
        user_message: str,
        file_controller: FileController,
        candidate_controller: CandidateController,
        knowledge_base_controller: KnowledgeBaseController,
        conversation_id: Optional[UUID] = None,
        candidate_id: Optional[UUID] = None,
    ):
        try:
            agent = self.compile(
                file_controller=file_controller,
                candidate_controller=candidate_controller,
                knowledge_base_controller=knowledge_base_controller,
                user=user,
            )

            if conversation_id is None:
                conversation_id = uuid4()
                yield f"event: conversationId\ndata: {conversation_id}\n\n"

            config: RunnableConfig = {"configurable": {"thread_id": conversation_id}}
            config = RunnableConfig(
                configurable={"thread_id": conversation_id},
                metadata={
                    "collection_name": KnowledgeBaseController._get_collection_name(
                        user
                    ),
                    "user_id": user.id.hex,
                },
            )

            messages: list[AnyMessage] = [HumanMessage(content=user_message)]

            agent_state: AgentState = {
                "messages": messages,
                "llm_calls": 0,
                "citations": [],
                "resume_retrieved_points": [],
                "candidate_retrieved_points": [],
                "candidates": [],
                "resume_candidates": [],
                "candidate_id": candidate_id.hex if candidate_id else None,
            }

            events = agent.stream(
                agent_state,
                config=config,
                stream_mode="updates",
            )

            yield f"event: node\ndata: __start__\n\n"

            for event in events:
                for node, event_value in event.items():
                    logger.debug(f"Node Finished: {node}")
                    yield f"event: node\ndata: {node}\n\n"

                    state = agent.get_state(config)
                    if len(state.next) != 0:
                        logger.debug(f"Current Node: {state.next}")
                        yield f"event: node\ndata: {state.next[0]}\n\n"

                    if event_value is None:
                        continue

                    messages = event_value.get("messages", [])
                    citations: Optional[list[BaseModel]] = event_value.get(
                        "citations", None
                    )
                    candidates: Optional[list[CandidateWithScore]] = event_value.get(
                        "candidates", None
                    )
                    resume_candidates: Optional[list[CandidateWithResume]] = (
                        event_value.get("resume_candidates", None)
                    )

                    if citations:
                        yield f"event: citations\ndata: {
                            json.dumps([c.model_dump() for c in citations], default=str)
                        }\n\n"

                    if candidates:
                        yield f"event: candidates\ndata: {
                            json.dumps(
                                [c.model_dump() for c in candidates], default=str
                            )
                        }\n\n"

                    if resume_candidates:
                        yield f"event: resume_candidates\ndata: {
                            json.dumps(
                                [c.model_dump() for c in resume_candidates], default=str
                            )
                        }\n\n"

                    if len(messages) == 0:
                        continue

                    message = messages[-1]

                    if isinstance(message, HumanMessage):
                        continue

                    elif isinstance(message, AIMessage):
                        reasoning_content = message.additional_kwargs.get(
                            "reasoning_content", None
                        )
                        if reasoning_content:
                            thinking_response = {"text": reasoning_content}
                            yield f"event: reason\ndata: {json.dumps(thinking_response)}\n\n"

                        response = {"text": message.content}
                        yield f"event: message\ndata: {json.dumps(response)}\n\n"

        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            yield f"event: error\ndata: {e}\n\n"
        finally:
            yield "event: done\ndata: end\n\n"
