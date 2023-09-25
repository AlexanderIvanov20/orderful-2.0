from pydantic import BaseModel, ConfigDict


class BaseProductAssociation(BaseModel):
    quantity: int | None = None
    product_id: int | None = None


class CreateProductAssociation(BaseProductAssociation):
    quantity: int
    product_id: int


class UpdateProductAssociation(CreateProductAssociation):
    pass


class ProductAssociation(CreateProductAssociation):
    model_config = ConfigDict(from_attributes=True)
