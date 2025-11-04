from uuid import UUID

import pymupdf
from celery.utils.log import get_task_logger

from celery import Celery
from src.core.config import settings
from src.core.dependencies import get_database_session
from src.core.exception import BadRequestException
from src.core.vector_db import vector_db_client
from src.models.models import Candidate, KnowledgeBaseDocument, User
from src.modules.candidate.controller import CandidateController
from src.modules.candidate.repository import CandidateRepository
from src.modules.candidate.schema import CandidateCreate
from src.modules.file_storage.controller import FileController
from src.modules.users.controller import UserController
from src.modules.users.repository import UserRepository
from src.utils.resume_parser import ResumeParser

logger = get_task_logger(__name__)

app = Celery(
    __name__,
    broker=settings.REDIS_URL,
    backend=settings.CELERY_BACKEND_URI,
)

app.conf.task_track_started = True
app.conf.result_extended = True
app.conf.database_create_tables_at_setup = True

session_generator = get_database_session()
session = next(session_generator)


@app.task(name="parse_document")
def parse_document(file_uri: str, file_id: UUID):
    file_path = FileController._get_local_file_path(file_name=file_uri)

    if not file_path.exists():
        raise Exception(f"File {file_uri} does not exists")

    doc = pymupdf.open(file_path.resolve())

    pages: list[str] = [page.get_text() for page in doc]  # type: ignore
    result = chr(12).join(pages)

    doc.close()

    from src.modules.knowledge_base.controller import KnowledgeBaseController
    from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository

    knowledge_base_controller = KnowledgeBaseController(
        repository=KnowledgeBaseDocumentRepository(
            model=KnowledgeBaseDocument, session=session
        ),
        vector_db=vector_db_client,
    )

    record = knowledge_base_controller.repository.upsert_by_file(file_id=file_id)
    record = knowledge_base_controller.repository.update(record.id, {"content": result})

    return result


@app.task(name="store_embedding")
def store_embeddings(content: str, file_id: UUID, user_id: UUID):
    user_controller = UserController(
        repository=UserRepository(model=User, session=session)
    )

    user = user_controller.get_by_id(user_id)

    from src.modules.knowledge_base.controller import KnowledgeBaseController
    from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository

    knowledge_base_controller = KnowledgeBaseController(
        repository=KnowledgeBaseDocumentRepository(
            model=KnowledgeBaseDocument, session=session
        ),
        vector_db=vector_db_client,
    )

    document = knowledge_base_controller.get_document_by_file_id(
        user=user, file_id=file_id
    )

    knowledge_base_controller.ingest_documents(user=user, files=[document.file])

    return document.id.hex


@app.task(name="create_candidate")
def create_candidate(knowledge_base_document_id: UUID):
    from src.modules.knowledge_base.controller import KnowledgeBaseController
    from src.modules.knowledge_base.repository import KnowledgeBaseDocumentRepository

    knowledge_base_controller = KnowledgeBaseController(
        repository=KnowledgeBaseDocumentRepository(
            model=KnowledgeBaseDocument, session=session
        ),
        vector_db=vector_db_client,
    )
    document = knowledge_base_controller.get_by_id(knowledge_base_document_id)
    content = document.content

    if content is None:
        raise BadRequestException(
            f"Knowledge base document {knowledge_base_document_id} does not have any content."
        )

    email = ResumeParser.extract_email_from_resume(content)
    name = ResumeParser.extract_name(content)
    contact = ResumeParser.extract_contact_number_from_resume(content)

    candidate_controller = CandidateController(
        repository=CandidateRepository(model=Candidate, session=session),
        vector_db=vector_db_client,
    )

    resume_parse = ResumeParser()
    output = resume_parse.extract_resume_details(content=content)

    if output.email != email:
        logger.info(
            f"Email extracted from model is different. Initial: {email}. Current: {output.email}"
        )

    if output.name != name:
        logger.info(
            f"Name extracted from model is different. Initial: {name}. Current: {output.name}"
        )

    if output.contact != contact:
        logger.info(
            f"Contact extracted from model is different. Initial: {contact}. Current: {output.contact}"
        )

    candidate = CandidateCreate(
        email=output.email,
        name=output.name,
        contact=output.contact,
        years_of_experience=output.years_of_experience,
        skills=output.skills,
        certifications=output.certifications,
        experiences=[e.model_dump(mode="json") for e in output.experiences],
        knowledge_base_document_id=knowledge_base_document_id,
    )

    candidate = candidate_controller.create(candidate)

    return candidate.model_dump_json()
