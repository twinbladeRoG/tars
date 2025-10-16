from uuid import UUID

from fastapi import APIRouter

from src.core.dependencies import CurrentUser
from src.core.factory.factory import UserControllerDeps

from .schema import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
def get_all_users(user_controller: UserControllerDeps, user: CurrentUser):
    users = user_controller.get_all(skip=0, limit=10)
    return users


@router.get("/{id}", response_model=UserPublic)
def get_user_by_id(id: UUID, user_controller: UserControllerDeps, user: CurrentUser):
    user = user_controller.get_by_id(id)
    return user


@router.post("/", response_model=UserPublic)
def create_user(user_controller: UserControllerDeps, user: UserCreate):
    response = user_controller.create(user)
    return response
