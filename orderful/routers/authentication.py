from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from orderful.models.users import User
from orderful.schemas import tokens as token_schemas
from orderful.schemas import users as user_schemas
from orderful.services.users import UserService, get_current_user, user_service

router = APIRouter(prefix="/authentication")


@router.post("/register", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def authorization(
    data: user_schemas.CreateUser,
    user_service: Annotated[UserService, Depends(user_service)],
):
    return user_service.authorize(data)


@router.post("/login", response_model=token_schemas.Token)
def authentication(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(user_service)],
):
    return user_service.authenticate(data.username, data.password)


@router.post("/validate-token", response_model=user_schemas.User)
def validate_token(user: Annotated[User, Depends(get_current_user)]):
    return user


# TODO: Implement password recovery.
