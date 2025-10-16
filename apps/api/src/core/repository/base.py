from typing import Any, Generic, Literal, Optional, Sequence, Type, TypeVar, overload

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, select

from src.core.exception import BadRequestException, NotFoundException
from src.models.mixins import BaseModelMixin

ModelType = TypeVar("ModelType", bound=BaseModelMixin)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session) -> None:
        self.session = session
        self.model_class: Type[ModelType] = model

    def create(self, attributes: Optional[dict[str, Any]] = None) -> ModelType:
        attributes = attributes or {}
        model = self.model_class(**attributes)

        try:
            self.session.add(model)
            self.session.commit()
            return model
        except IntegrityError:
            raise BadRequestException(
                f"Cannot create {self.model_class.__name__}",
                error_code="IntegrityError",
            )
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        statement = select(self.model_class).offset(skip).limit(limit)
        results = self.session.exec(statement).all()
        return results

    @overload
    def get_by(self, field: str, value: Any, *, unique: Literal[True]) -> ModelType: ...

    @overload
    def get_by(
        self, field: str, value: Any, *, unique: Literal[False] = False
    ) -> Sequence[ModelType]: ...

    def get_by(self, field: str, value: Any, *, unique: bool = False):
        query = self._query()
        query = query.where(getattr(self.model_class, field) == value)
        result = self.session.exec(query)

        if unique:
            try:
                return result.one()
            except NoResultFound:
                raise NotFoundException(
                    f"{self.model_class.__name__} has no matching row"
                )
        return result.all()

    def delete(self, model: ModelType) -> None:
        self.session.delete(model)

    def _query(self):
        query = select(self.model_class)
        return query
