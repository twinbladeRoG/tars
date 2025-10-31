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

from src.core.logger import logger
from src.models.models import User

from .nodes.chatbot import ChatBotNode
from .nodes.retrieval import RetrievalNode
from .state import AgentState


class RootAgent:
    def __init__(self) -> None:
        self.memory = MemorySaver()
        self.agent = None

    def compile(self):
        if self.agent is not None:
            logger.debug("Agent already complied")
            return self.agent

        agent_builder = StateGraph(AgentState)

        # Add Nodes
        agent_builder.add_node("chatbot", ChatBotNode())
        agent_builder.add_node("vector_search", RetrievalNode())

        # Add Edges
        agent_builder.add_edge(START, "vector_search")
        agent_builder.add_edge("vector_search", "chatbot")
        agent_builder.add_edge("chatbot", END)

        agent = agent_builder.compile(checkpointer=self.memory)
        self.agent = agent
        return agent

    def stream(
        self,
        *,
        user: User,
        user_message: str,
        conversation_id: Optional[UUID | None] = None,
    ):
        try:
            agent = self.compile()

            if conversation_id is None:
                conversation_id = uuid4()
                yield f"event: conversationId\ndata: {conversation_id}\n\n"

            config: RunnableConfig = {"configurable": {"thread_id": conversation_id}}
            config = RunnableConfig(
                configurable={"thread_id": conversation_id},
                metadata={"collection_name": f"{user.first_name}_{user.id}"},
            )

            messages: list[AnyMessage] = [HumanMessage(content=user_message)]
            agent_state: AgentState = {
                "messages": messages,
                "llm_calls": 0,
                "retrieved_points": [],
            }

            events = agent.stream(
                agent_state,
                config=config,
                stream_mode="updates",
            )

            yield f"event: node\ndata: vector_search\n\n"

            for event in events:
                for node, event_value in event.items():
                    logger.debug(f"Node Finished: {node}")
                    yield f"event: node\ndata: {node}\n\n"

                    state = agent.get_state(config)
                    if len(state.next) != 0:
                        logger.debug(f"Current Node: {state.next[0]}")
                        yield f"event: node\ndata: {state.next[0]}\n\n"

                    messages = event_value.get("messages", [])

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
