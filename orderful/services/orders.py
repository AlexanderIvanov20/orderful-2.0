import random
import string
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from orderful.core.dependencies import get_session
from orderful.models.associations import OrderProductAssociation
from orderful.models.orders import Order
from orderful.schemas.orders import CreateOrder, UpdateOrder
from orderful.services.associations_base import AssociationsMixin
from orderful.services.base import BaseService


class OrderService(AssociationsMixin, BaseService[Order, CreateOrder, UpdateOrder]):
    model: type[Order] = Order

    @staticmethod
    def get_order_code():
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=20))

    def create(self, data: CreateOrder, **kwargs: Any) -> Order:
        data.code = self.get_order_code()

        return super().create(data, **kwargs)

    def save_with_associations(
        self,
        data: CreateOrder | UpdateOrder,
        associated_id: int,
        associated_field: str,
        instance_name: str,
        associated_service: BaseService,
        association_model: OrderProductAssociation,
        instance: Order = None,
        **kwargs: Any,
    ) -> Order:
        kwargs.setdefault("code", self.get_order_code())
        return super().save_with_associations(
            data,
            associated_id,
            associated_field,
            instance_name,
            associated_service,
            association_model,
            instance,
            **kwargs,
        )


def order_service(session: Annotated[Session, Depends(get_session)]):
    return OrderService(session)
