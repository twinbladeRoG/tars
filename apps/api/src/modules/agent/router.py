from fastapi import APIRouter

from src.core.factory.factory import AgentControllerDeps

from .schema import AgentWorkflowResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/workflow", response_model=AgentWorkflowResponse)
def get_agent(agent_controller: AgentControllerDeps):
    state, mermaid = agent_controller.get_workflow()
    return AgentWorkflowResponse(mermaid=mermaid, state=state)
