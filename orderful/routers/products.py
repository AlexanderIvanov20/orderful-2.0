from typing import Annotated

from fastapi import APIRouter, Depends, status

from orderful.core.settings import settings
from orderful.models.users import User
from orderful.schemas import products as schemas
from orderful.services.products import ProductService, product_service
from orderful.services.users import get_current_active_user

router = APIRouter(prefix="/products")


@router.get("/", response_model=list[schemas.Product])
def get_products(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    offset: int = settings.OFFSET,
    limit: int = settings.LIMIT,
):
    return product_service.get_products_by_user(active_user, offset, limit)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    data: schemas.CreateProduct,
):
    return product_service.create(data, user_id=active_user.id)


@router.get("/{id}", response_model=schemas.Product)
def get_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    id: int,
):
    return product_service.get_product(id, active_user)


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    data: schemas.UpdateProduct,
    id: int,
):
    product = product_service.get_product(id, active_user)
    return product_service.update(product, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    id: int,
):
    product = product_service.get_product(id, active_user)
    product_service.delete(product.id)
