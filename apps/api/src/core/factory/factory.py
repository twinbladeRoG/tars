from functools import partial
from typing import Annotated

from fastapi import Depends

from src.core.dependencies import SessionDep
from src.models.models import User
from src.modules.agent.controller import AgentController
from src.modules.auth.controller import AuthController
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository


class Factory:
    user_repository = partial(UserRepository, User)

    def get_user_controller(self, db_session: SessionDep):
        return UserController(repository=self.user_repository(session=db_session))

    def get_auth_controller(self, db_session: SessionDep):
        return AuthController(repository=self.user_repository(session=db_session))

    def get_agent_controller(self):
        return AgentController()


UserControllerDeps = Annotated[UserController, Depends(Factory().get_user_controller)]
AuthControllerDeps = Annotated[AuthController, Depends(Factory().get_auth_controller)]
AgentControllerDeps = Annotated[
    AgentController, Depends(Factory().get_agent_controller)
]
