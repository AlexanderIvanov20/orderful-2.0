from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from orderful.core.dependencies import get_session
from orderful.core.security import PasswordServiceMixin, TokenServiceMixin, oauth2_scheme
from orderful.core.settings import settings
from orderful.models.users import User
from orderful.schemas.tokens import Token
from orderful.schemas.users import CreateUser, UpdateUser
from orderful.services.base import BaseService


class UserService(PasswordServiceMixin, TokenServiceMixin, BaseService[User, CreateUser, UpdateUser]):
    model: type[User] = User

    def get_instance_by_user(self, id: int, current_user: User) -> User | None:
        instance = self.get_instance(id)

        if not current_user.superuser and instance.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The current user does not have enough privileges.",
            )

        return instance

    def authenticate(self, email: str, password: str) -> Token | None:
        user = self.filter_by(email=email).first()

        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or password is invalid.",
            )

        access_token = self.create_access_token(user.id)
        return Token(access_token=access_token, token_type=settings.TOKEN_TYPE)

    def authorize(self, data: CreateUser) -> User:
        if self.session.query(self.filter_by(email=data.email).exists()).scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The user with email={data.email} already exists.",
            )

        return self.create(data)

    def verify_token(self, token: str) -> User:
        token_data = self.get_token_data(token, settings.SECRET_KEY, authenticate_value="Bearer")
        return self.get(token_data.sub)

    def create(self, data: CreateUser, **kwargs: Any) -> User:
        data.password = self.get_password_hash(data.password)

        return super().create(data, **kwargs)

    def update(self, instance: User, data: UpdateUser, **kwargs: Any) -> User:
        if password := data.password:
            data.password = self.get_password_hash(password)

        return super().update(instance, data, **kwargs)


def user_service(session: Annotated[Session, Depends(get_session)]):
    return UserService(session)


def get_current_user(
    user_service: Annotated[UserService, Depends(user_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    user = user_service.verify_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist.",
        )

    return user


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The current user is inactive.",
        )

    return user


def get_current_active_superuser(user: Annotated[User, Depends(get_current_active_user)]):
    if not user.superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The current user does not have enough privileges.",
        )

    return user
