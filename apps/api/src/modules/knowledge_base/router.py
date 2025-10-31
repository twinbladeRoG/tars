from fastapi import APIRouter

from src.core.dependencies import CurrentUser
from src.core.factory.factory import FileControllerDeps, KnowledgeBaseControllerDeps
from src.models.models import KnowledgeBaseDocument

from .schema import DocumentExtractionRequest, IngestDocumentRequest

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])


@router.post("/", response_model=KnowledgeBaseDocument)
def enqueue_document(
    body: DocumentExtractionRequest,
    knowledge_base_controller: KnowledgeBaseControllerDeps,
    file_controller: FileControllerDeps,
    user: CurrentUser,
):
    document = file_controller.get_file_by_id(body.file_id, user.id)
    knowledge_base_document = knowledge_base_controller.enqueue_document(
        document=document
    )
    return knowledge_base_document


@router.get("/status/{id}", response_model=KnowledgeBaseDocument)
def task_status(id: str, knowledge_base_controller: KnowledgeBaseControllerDeps):
    return knowledge_base_controller.get_task_status(id)


@router.post("/ingest")
def ingest(
    body: IngestDocumentRequest,
    user: CurrentUser,
    knowledge_base_controller: KnowledgeBaseControllerDeps,
    file_controller: FileControllerDeps,
):
    documents = file_controller.get_files_by_id(ids=body.documents, user_id=user.id)
    return knowledge_base_controller.ingest_documents(user, documents)
