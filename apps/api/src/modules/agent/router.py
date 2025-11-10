from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.core.dependencies import CurrentUser
from src.core.factory.factory import (
    AgentControllerDeps,
    CandidateControllerDeps,
    FileControllerDeps,
    KnowledgeBaseControllerDeps,
)

from .schema import AgentChatRequest, AgentWorkflowResponse

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/workflow", response_model=AgentWorkflowResponse)
def get_agent(
    user: CurrentUser,
    agent_controller: AgentControllerDeps,
    file_controller: FileControllerDeps,
    candidate_controller: CandidateControllerDeps,
    knowledge_base_controller: KnowledgeBaseControllerDeps,
):
    state, mermaid = agent_controller.get_workflow(
        file_controller=file_controller,
        candidate_controller=candidate_controller,
        knowledge_base_controller=knowledge_base_controller,
        user=user,
    )
    return AgentWorkflowResponse(mermaid=mermaid, state=state)


@router.post("/chat")
def chat(
    user: CurrentUser,
    body: AgentChatRequest,
    agent_controller: AgentControllerDeps,
    file_controller: FileControllerDeps,
    candidate_controller: CandidateControllerDeps,
    knowledge_base_controller: KnowledgeBaseControllerDeps,
):
    return StreamingResponse(
        agent_controller.stream(
            user=user,
            conversation_id=body.conversation_id,
            user_message=body.message,
            candidate_id=body.candidate_id,
            file_controller=file_controller,
            candidate_controller=candidate_controller,
            knowledge_base_controller=knowledge_base_controller,
        ),
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        },
    )
