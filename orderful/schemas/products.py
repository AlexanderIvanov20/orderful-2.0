from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CategoryAssociation(BaseModel):
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class BaseProduct(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    article: str | None = None
    quantity: int | None = None
    categories: list[int] = []


class CreateProduct(BaseProduct):
    name: str
    price: Decimal
    article: str
    quantity: int
    categories: list[int]


class UpdateProduct(CreateProduct):
    pass


class Product(CreateProduct):
    id: int
    user_id: int
    categories: list[CategoryAssociation]

    model_config = ConfigDict(from_attributes=True)
