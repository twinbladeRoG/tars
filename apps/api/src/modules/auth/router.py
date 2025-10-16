from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.dependencies import CurrentUser, TokenDep
from src.core.factory.factory import AuthControllerDeps
from src.modules.users.schema import UserPublic

from .schema import Tokens, TokenWithUser

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenWithUser)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_controller: AuthControllerDeps,
):
    user, tokens = auth_controller.login(
        email=form_data.username, password=form_data.password
    )
    return TokenWithUser(user=UserPublic.model_validate(user), tokens=tokens)


@router.get("/refresh", response_model=Tokens)
def refresh(token: TokenDep, auth_controller: AuthControllerDeps):
    return auth_controller.generate_fresh_tokens(token)


@router.get("/verify", response_model=UserPublic)
def verify(user: CurrentUser):
    return user
