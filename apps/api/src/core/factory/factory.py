from functools import partial
from typing import Annotated

from fastapi import Depends

from src.core.dependencies import SessionDep
from src.models.models import File, User
from src.modules.agent.controller import AgentController
from src.modules.auth.controller import AuthController
from src.modules.file_storage.controller import FileController
from src.modules.file_storage.repository import FileRepository
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository


class Factory:
    user_repository = partial(UserRepository, User)
    file_repository = partial(FileRepository, File)

    def get_user_controller(self, db_session: SessionDep):
        return UserController(repository=self.user_repository(session=db_session))

    def get_auth_controller(self, db_session: SessionDep):
        return AuthController(repository=self.user_repository(session=db_session))

    def get_agent_controller(self):
        return AgentController()

    def get_file_controller(self, db_session: SessionDep):
        return FileController(repository=self.file_repository(session=db_session))


UserControllerDeps = Annotated[UserController, Depends(Factory().get_user_controller)]
AuthControllerDeps = Annotated[AuthController, Depends(Factory().get_auth_controller)]
AgentControllerDeps = Annotated[
    AgentController, Depends(Factory().get_agent_controller)
]
FileControllerDeps = Annotated[FileController, Depends(Factory().get_file_controller)]
