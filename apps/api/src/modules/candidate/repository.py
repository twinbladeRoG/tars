from uuid import UUID

from src.core.repository.base import BaseRepository
from src.models.models import Candidate


class CandidateRepository(BaseRepository[Candidate]):
    def get_by_email(self, email: str) -> Candidate:
        return self.get_by("email", email, unique=True)

    def get_by_knowledge_base_id(self, knowledge_base_id: UUID):
        statement = self._query().where(
            self.model_class.knowledge_base_document_id == knowledge_base_id
        )

        record = self.session.exec(statement).one_or_none()
        return record
