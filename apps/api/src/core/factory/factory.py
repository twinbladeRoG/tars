from functools import partial
from typing import Annotated

from fastapi import Depends

from src.core.dependencies import SessionDep, VectorDatabaseDep
from src.models.models import File, KnowledgeBaseDocument, User
from src.modules.agent.controller import AgentController
from src.modules.auth.controller import AuthController
from src.modules.file_storage.controller import FileController
from src.modules.file_storage.repository import FileRepository
from src.modules.knowledge_base.controller import KnowledgeBaseController
from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository


class Factory:
    user_repository = partial(UserRepository, User)
    file_repository = partial(FileRepository, File)
    knowledge_base_document_repository = partial(
        KnowledgeBaseDocumentRepository, KnowledgeBaseDocument
    )

    def get_user_controller(self, db_session: SessionDep):
        return UserController(repository=self.user_repository(session=db_session))

    def get_auth_controller(self, db_session: SessionDep):
        return AuthController(repository=self.user_repository(session=db_session))

    def get_agent_controller(self):
        return AgentController()

    def get_file_controller(self, db_session: SessionDep):
        return FileController(repository=self.file_repository(session=db_session))

    def get_knowledge_base_controller(
        self, vector_db: VectorDatabaseDep, db_session: SessionDep
    ):
        return KnowledgeBaseController(
            repository=self.knowledge_base_document_repository(session=db_session),
            vector_db=vector_db,
        )


UserControllerDeps = Annotated[UserController, Depends(Factory().get_user_controller)]
AuthControllerDeps = Annotated[AuthController, Depends(Factory().get_auth_controller)]
AgentControllerDeps = Annotated[
    AgentController, Depends(Factory().get_agent_controller)
]
FileControllerDeps = Annotated[FileController, Depends(Factory().get_file_controller)]
KnowledgeBaseControllerDeps = Annotated[
    KnowledgeBaseController, Depends(Factory().get_knowledge_base_controller)
]
