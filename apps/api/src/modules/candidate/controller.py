from src.core.controller.base import BaseController
from src.models.models import Candidate

from .repository import CandidateRepository


class CandidateController(BaseController[Candidate]):
    def __init__(self, repository: CandidateRepository) -> None:
        super().__init__(model=Candidate, repository=repository)
        self.repository = repository
