from src.core.controller.base import BaseController
from src.models.models import Candidate, File, KnowledgeBaseDocument, User

from .repository import CandidateRepository


class CandidateController(BaseController[Candidate]):
    def __init__(self, repository: CandidateRepository) -> None:
        super().__init__(model=Candidate, repository=repository)
        self.repository = repository

    def get_candidates(self, user: User):
        statement = (
            self.repository._query()
            .join(Candidate.knowledge_base_document)  # type: ignore
            .join(KnowledgeBaseDocument.file)  # type: ignore
            .join(File.owner)  # type: ignore
            .where(User.id == user.id)
        )

        candidates = self.repository.session.exec(statement).all()
        return list(candidates)
