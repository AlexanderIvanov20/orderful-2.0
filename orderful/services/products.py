from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from orderful.core.dependencies import get_session
from orderful.models.categories import Category
from orderful.models.products import Product
from orderful.schemas.products import CreateProduct, UpdateProduct
from orderful.services.associations_base import AssociationsMixin
from orderful.services.base import BaseService


class ProductService(AssociationsMixin, BaseService[Product, CreateProduct, UpdateProduct]):
    model: type[Product] = Product

    @staticmethod
    def _extract_ids_from_associations(associated_id: int, associations: list[dict[str, Any]]) -> list[int]:
        return associations

    @staticmethod
    def _prepare_association_instance(
        association: Category, association_model: type[Product], instance_name: str, instance: Product
    ) -> dict[str, Any]:
        return association_model(category_id=association, product=instance)


def product_service(session: Annotated[Session, Depends(get_session)]):
    return ProductService(session)
