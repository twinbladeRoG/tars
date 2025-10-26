from math import ceil
from typing import Generic, TypeVar

from sqlmodel import SQLModel


class Pagination(SQLModel):
    page: int
    limit: int
    total_pages: int
    total_count: int
    has_next: bool
    has_previous: bool


def get_pagination(page: int, limit: int, count: int) -> Pagination:
    total_pages = ceil(count / limit)

    pagination = Pagination(
        page=page,
        limit=limit,
        total_count=count,
        total_pages=total_pages,
        has_next=True if page != total_pages - 1 and page < total_pages - 1 else False,
        has_previous=True if page != 0 and page <= total_pages - 1 else False,
    )

    return pagination


T = TypeVar("T", bound=SQLModel)


class ModelPaginated(SQLModel, Generic[T]):
    data: list[T]
    pagination: Pagination
