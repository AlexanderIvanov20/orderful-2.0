import random
import string
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Query, Session

from orderful.core.dependencies import get_session
from orderful.models.associations import OrderProductAssociation
from orderful.models.orders import Order
from orderful.models.products import Product
from orderful.models.users import User
from orderful.schemas.orders import CreateOrder, UpdateOrder
from orderful.services.base import BaseService
from orderful.services.products import ProductService


class OrderService(BaseService[Order, CreateOrder, UpdateOrder]):
    model: Order = Order

    @staticmethod
    def get_order_code():
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))

    def get_orders_by_user(self, current_user: User, offset: int, limit: int) -> Query[Order]:
        if current_user.superuser:
            return self.paginate(offset, limit).all()

        return self.paginate(offset, limit).filter_by(user_id=current_user.id).all()

    # TODO: Move the pattern to base.
    def get_order(self, current_user: User, id: int) -> Order:
        order = self.get(id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The order with id={id} does not exist.",
            )

        if not current_user.superuser and order.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The current user does not have enough privileges.",
            )

        return order

    def create(self, data: CreateOrder, **kwargs: Any) -> Order:
        data.code = self.get_order_code()

        return super().create(data, **kwargs)

    def create_with_products(self, data: CreateOrder, **kwargs: Any) -> Order:
        data = data.model_dump(exclude_unset=True, exclude=[])

        product_associations = data.pop("products")
        product_ids = [association["product_id"] for association in product_associations]
        products = ProductService(self.session).filter(Product.id.in_(product_ids)).all()

        if non_existing_product_ids := set(product_ids) - {product.id for product in products}:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The product(s) with the ids={non_existing_product_ids} do(es) not exist.",
            )

        instance = self.model(code=self.get_order_code(), **data, **kwargs)
        associations = [
            OrderProductAssociation(**association, order=instance) for association in product_associations
        ]

        self.session.add_all([instance, *associations])
        self.session.commit()

        return instance


def order_service(session: Annotated[Session, Depends(get_session)]):
    return OrderService(session)
