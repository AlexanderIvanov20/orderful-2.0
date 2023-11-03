from abc import abstractmethod
from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Query, Session

from orderful.core.settings import settings
from orderful.models.base import Base
from orderful.models.users import User

T = TypeVar("T", bound="BaseService")
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SessionMixin:
    def __init__(self, session: Session) -> None:
        self.session = session

    @property
    @abstractmethod
    def model(self) -> type[ModelType]:
        pass


class BaseReadOnlyService(SessionMixin, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
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

    def get_instance(self, id: int) -> ModelType | None:
        instance = self.get(id)

        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The instance with id={id} does not exist.",
            )

        return instance

    def get_instances_by_user(self, offset: int, limit: int, current_user: User) -> Query[ModelType]:
        if current_user.superuser:
            return self.paginate(offset, limit).all()

        return self.filter_by(user_id=current_user.id).offset(offset).limit(limit).all()

    def get_instance_by_user(self, id: int, current_user: User) -> ModelType | None:
        instance = self.get_instance(id)

        if not current_user.superuser and instance.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The current user does not have enough privileges.",
            )

        return instance


class BaseService(BaseReadOnlyService, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def create(self, data: CreateSchemaType | dict[str, Any], **kwargs: Any) -> ModelType:
        instance = self.model(**jsonable_encoder(data), **kwargs)

        self.session.add(instance)
        self.session.commit()

        return instance

    def update(
        self, instance: ModelType, data: UpdateSchemaType | dict[str, Any], **kwargs: Any
    ) -> ModelType:
        data = data.model_dump(exclude_unset=True) if not isinstance(data, dict) else data

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
