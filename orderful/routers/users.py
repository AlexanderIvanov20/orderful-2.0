from typing import Annotated

from fastapi import APIRouter, Depends, status

from orderful.core.settings import settings
from orderful.models.users import User
from orderful.schemas import users as schemas
from orderful.services.users import UserService, get_current_active_user, user_service

router = APIRouter(prefix="/users")


@router.get("/me", response_model=schemas.User)
def get_me(active_user: Annotated[User, Depends(get_current_active_user)]):
    return active_user


@router.get("/", response_model=list[schemas.User])
def get_users(
    active_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(user_service)],
    offset: int = settings.OFFSET,
    limit: int = settings.LIMIT,
):
    return user_service.paginate(offset, limit)


@router.get("/{id}", response_model=schemas.User)
def get_user(
    active_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(user_service)],
    id: int,
):
    return user_service.get_user(id, active_user)


@router.put("/{id}", response_model=schemas.User)
def update_user(
    active_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(user_service)],
    data: schemas.UpdateUser,
    id: int,
):
    user = user_service.get_user(id, active_user)
    return user_service.update(user, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    active_user: Annotated[User, Depends(get_current_active_user)],
    user_service: Annotated[UserService, Depends(user_service)],
    id: int,
):
    user = user_service.get_user(id, active_user)
    user_service.delete(user.id)
