from decimal import Decimal

from pydantic import BaseModel, ConfigDict


# TODO: Add the categories.
class BaseProduct(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    article: str | None = None
    quantity: int | None = None


class CreateProduct(BaseProduct):
    name: str
    price: Decimal
    article: str
    quantity: int


class UpdateProduct(CreateProduct):
    pass


class Product(CreateProduct):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
