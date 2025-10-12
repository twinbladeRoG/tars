from fastapi import APIRouter

from src.core.dependencies import SessionDep

from .schema import UserPublic
from .service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
def get_all_users(session: SessionDep):
    service = UserService()
    users = service.get_users(session)
    return users
