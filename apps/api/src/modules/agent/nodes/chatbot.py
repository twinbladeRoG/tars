from src.modules.llm_models.model import LlmModelFactory

from ..state import AgentState


class ChatBotNode:
    def __init__(self):
        self.model_factory = LlmModelFactory()
        self.llm = self.model_factory.get_model("deepseek-r1")
        self.llm = self.llm.bind_tools([])

    def __call__(self, state: AgentState):
        response = self.llm.invoke(state["messages"])
        return {"messages": [response]}
