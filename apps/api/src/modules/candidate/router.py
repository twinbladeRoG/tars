from uuid import UUID

from fastapi import APIRouter

from src.core.factory.factory import CandidateControllerDeps
from src.models.models import CandidateWithKnowledgeBase

router = APIRouter(prefix="/candidate", tags=["Candidates"])


@router.get("/{candidate_id}", response_model=CandidateWithKnowledgeBase)
def get_candidate(candidate_id: UUID, candidate_controller: CandidateControllerDeps):
    return candidate_controller.get_by_id(candidate_id)
