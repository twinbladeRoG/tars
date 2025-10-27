from uuid import UUID

from fastapi import APIRouter, UploadFile

from src.core.dependencies import CurrentUser
from src.core.factory.factory import FileControllerDeps
from src.models.models import File
from src.models.pagination import ModelPaginated

router = APIRouter(prefix="/file-storage", tags=["File Storage"])


class FilePaginated(ModelPaginated[File]):
    data: list[File]


@router.get("/", response_model=FilePaginated)
def get_all_files(
    file_controller: FileControllerDeps,
    user: CurrentUser,
    page: int = 0,
    limit: int = 10,
):
    files, pagination = file_controller.get_users_files(user.id, page, limit)
    return FilePaginated(data=list(files), pagination=pagination)


@router.post("/", response_model=File)
async def create_file(
    file: UploadFile,
    user: CurrentUser,
    file_controller: FileControllerDeps,
):
    return await file_controller.upload(user_id=user.id, file=file)


@router.get("/{file_id}", response_model=File)
def get_file(
    file_controller: FileControllerDeps,
    user: CurrentUser,
    file_id: UUID,
):
    return file_controller.get_file_by_id(id=file_id, user_id=user.id)


@router.delete("/{file_id}")
def delete_file(
    file_id: UUID,
    file_controller: FileControllerDeps,
    user: CurrentUser,
):
    return file_controller.remove_file(id=file_id, user_id=user.id)
