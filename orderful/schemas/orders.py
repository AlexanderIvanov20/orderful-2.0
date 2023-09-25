from datetime import datetime

from pydantic import BaseModel, ConfigDict

from orderful.models.orders import Order
from orderful.schemas.product_associations import ProductAssociation


class BaseOrder(BaseModel):
    code: str | None = None
    start_date: datetime | None = None
    status: Order.Status | None = None


class CreateOrder(BaseOrder):
    start_date: datetime
    status: Order.Status
    products: list[ProductAssociation]


class UpdateOrder(BaseOrder):
    pass


class Order(CreateOrder):
    id: int
    user_id: int
    products: list[ProductAssociation]

    model_config = ConfigDict(from_attributes=True)
