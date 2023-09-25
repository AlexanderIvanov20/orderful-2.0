from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Query, Session

from orderful.core.settings import settings
from orderful.models.base import Base

T = TypeVar("T", bound="BaseService")
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: type[ModelType]

    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> list[ModelType]:
        return self.session.query(self.model).all()

    def get(self, id: int) -> ModelType | None:
        return self.session.query(self.model).get(id)

    def filter(self, *filters: Any) -> Query[ModelType]:
        return self.session.query(self.model).filter(*filters)

    def filter_by(self, **filters: dict[str, Any]) -> Query[ModelType]:
        return self.session.query(self.model).filter_by(**filters)

    def paginate(self, offset: int = settings.OFFSET, limit: int = settings.LIMIT) -> Query[ModelType]:
        return self.session.query(self.model).offset(offset).limit(limit)

    def create(self, data: CreateSchemaType, **kwargs: Any) -> ModelType:
        instance = self.model(**jsonable_encoder(data), **kwargs)

        self.session.add(instance)
        self.session.commit()

        return instance

    def update(self, instance: ModelType, data: UpdateSchemaType, **kwargs: Any) -> ModelType:
        data = data.model_dump(exclude_unset=True)

        for field in jsonable_encoder(instance):
            if field in data:
                setattr(instance, field, data[field])

        self.session.add(instance)
        self.session.commit()

        return instance

    def delete(self, id: int) -> ModelType:
        instance = self.get(id)

        self.session.delete(instance)
        self.session.commit()

        return instance
