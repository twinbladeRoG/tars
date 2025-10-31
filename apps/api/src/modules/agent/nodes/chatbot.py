from langchain.messages import SystemMessage

from src.modules.llm_models.model import LlmModelFactory

from ..state import AgentState


class ChatBotNode:
    def __init__(self):
        self.model_factory = LlmModelFactory()
        self.llm = self.model_factory.get_model("deepseek-r1")
        self.llm = self.llm.bind_tools([])

    def __call__(self, state: AgentState):
        results = state["retrieved_points"]
        retrieved_texts = ""

        if results is not None:
            for point in results:
                if point.payload:
                    retrieved_texts += "\n" + point.payload["text"]

        system_prompt = f"""
        <Retrieved Results>
        {retrieved_texts}
        """

        response = self.llm.invoke(
            [SystemMessage(content=system_prompt)] + state["messages"]
        )
        return {"messages": [response]}
