from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from orderful.core.dependencies import get_session
from orderful.models.categories import Category
from orderful.services.base import BaseReadOnlyService


class CategoryService(BaseReadOnlyService):
    model: type[Category] = Category


def category_service(session: Annotated[Session, Depends(get_session)]):
    return CategoryService(session)
