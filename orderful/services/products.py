from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Query, Session

from orderful.core.dependencies import get_session
from orderful.models.products import Product
from orderful.models.users import User
from orderful.schemas.products import CreateProduct, UpdateProduct
from orderful.services.base import BaseService


class ProductService(BaseService[Product, CreateProduct, UpdateProduct]):
    model: Product = Product

    def get_products_by_user(self, current_user: User, offset: int, limit: int) -> Query[Product]:
        if current_user.superuser:
            return self.paginate(offset, limit).all()

        return self.paginate(offset, limit).filter_by(user_id=current_user.id).all()

    def get_product(self, id: int, current_user: User) -> Product:
        product = self.get(id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product with id={id} does not exist.",
            )

        if not current_user.superuser and product.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The current user does not have enough privileges.",
            )

        return product


def product_service(session: Annotated[Session, Depends(get_session)]):
    return ProductService(session)
