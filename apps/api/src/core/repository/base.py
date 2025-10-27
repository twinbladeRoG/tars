from typing import Any, Generic, Literal, Optional, Sequence, Type, TypeVar, overload
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlmodel import Session, func, select

from src.core.exception import BadRequestException, NotFoundException
from src.core.logger import logger
from src.models.mixins import BaseModelMixin

ModelType = TypeVar("ModelType", bound=BaseModelMixin)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Session) -> None:
        self.session = session
        self.model_class: Type[ModelType] = model

    def create(self, attributes: Optional[dict[str, Any]] = None) -> ModelType:
        attributes = attributes or {}

        try:
            model = self.model_class.model_validate(attributes)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except IntegrityError as e:
            logger.error(e._message)
            raise BadRequestException(
                f"Cannot create {self.model_class.__name__}",
                error_code="IntegrityError",
            )
        except Exception as e:
            logger.error(e)
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
        self.session.commit()

    def _query(self):
        query = select(self.model_class)
        return query

    def count(self):
        statement = select(func.count()).select_from(self.model_class)
        count = self.session.exec(statement).one()
        return count

    def update(
        self, id: UUID, attributes: Optional[dict[str, Any]] = None
    ) -> ModelType:
        attributes = attributes or {}
        model = self.get_by("id", id, unique=True)

        try:
            for key, value in attributes.items():
                setattr(model, key, value)

            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return model
        except IntegrityError as e:
            logger.error(e._message)
            raise BadRequestException(
                f"Cannot create {self.model_class.__name__}",
                error_code="IntegrityError",
            )
        except Exception as e:
            logger.error(e)
            self.session.rollback()
            raise e
