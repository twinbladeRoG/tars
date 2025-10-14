from functools import partial
from typing import Annotated

from fastapi import Depends

from src.core.dependencies import SessionDep
from src.models.models import User
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository


class Factory:
    user_repository = partial(UserRepository, User)

    def get_user_controller(self, db_session: SessionDep):
        return UserController(repository=self.user_repository(session=db_session))


UserRepositoryDeps = Annotated[UserController, Depends(Factory().get_user_controller)]
