from uuid import UUID

from fastapi import APIRouter

from src.core.dependencies import CurrentUser
from src.core.factory.factory import CandidateControllerDeps
from src.models.models import Candidate

router = APIRouter(prefix="/candidate", tags=["Candidates"])


@router.get("/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: UUID, candidate_controller: CandidateControllerDeps):
    return candidate_controller.get_by_id(candidate_id)


@router.get("/", response_model=list[Candidate])
def get_candidates(
    user: CurrentUser,
    candidate_controller: CandidateControllerDeps,
):
    return candidate_controller.get_candidates(user)
