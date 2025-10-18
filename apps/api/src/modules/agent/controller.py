from typing import Any

from .agent import RootAgent


class AgentController:
    def __init__(self) -> None:
        self.agent = RootAgent()

    def __call__(self) -> Any:
        pass

    def get_workflow(self):
        agent = self.agent.compile()
        mermaid = agent.get_graph(xray=True).draw_mermaid()
        state = agent.get_graph(xray=True).to_json()

        return state, mermaid

    def stream(self):
        pass
