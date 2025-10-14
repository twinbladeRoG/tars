from uuid import UUID

from fastapi import APIRouter

from src.core.dependencies import SessionDep
from src.core.repository.factory import UserRepositoryDeps

from .schema import UserPublic
from .service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
def get_all_users(session: SessionDep):
    service = UserService()
    users = service.get_users(session)
    return users


@router.get("/{id}", response_model=UserPublic)
def get_user_by_id(
    id: UUID,
    user_controller: UserRepositoryDeps,
):
    user = user_controller.get_by_id(id)

    return user
