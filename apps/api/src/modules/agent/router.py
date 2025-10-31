from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.core.dependencies import CurrentUser
from src.core.factory.factory import AgentControllerDeps

from .schema import AgentChatRequest, AgentWorkflowResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/workflow", response_model=AgentWorkflowResponse)
def get_agent(user: CurrentUser, agent_controller: AgentControllerDeps):
    state, mermaid = agent_controller.get_workflow()
    return AgentWorkflowResponse(mermaid=mermaid, state=state)


@router.post("/chat")
def chat(
    agent_controller: AgentControllerDeps, user: CurrentUser, body: AgentChatRequest
):
    return StreamingResponse(
        agent_controller.stream(
            user=user, conversation_id=body.conversation_id, user_message=body.message
        ),
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        },
    )
