from typing import Annotated

from fastapi import APIRouter, Depends, status

from orderful.core.settings import settings
from orderful.models.associations import CategoryProductAssociation
from orderful.models.users import User
from orderful.schemas import products as schemas
from orderful.services.categories import CategoryService, category_service
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
    return product_service.get_instances_by_user(offset, limit, active_user)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(category_service)],
    product_service: Annotated[ProductService, Depends(product_service)],
    data: schemas.CreateProduct,
):
    return product_service.save_with_associations(
        data,
        "category_id",
        "categories",
        "product",
        category_service,
        CategoryProductAssociation,
        user_id=active_user.id,
    )


@router.get("/{id}", response_model=schemas.Product)
def get_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    id: int,
):
    return product_service.get_instance_by_user(id, active_user)


@router.put("/{id}", response_model=schemas.Product)
def update_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    category_service: Annotated[CategoryService, Depends(category_service)],
    product_service: Annotated[ProductService, Depends(product_service)],
    data: schemas.UpdateProduct,
    id: int,
):
    product = product_service.get_instance_by_user(id, active_user)
    return product_service.save_with_associations(
        product,
        data,
        "category_id",
        "categories",
        "product",
        category_service,
        CategoryProductAssociation,
        instance=product,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    active_user: Annotated[User, Depends(get_current_active_user)],
    product_service: Annotated[ProductService, Depends(product_service)],
    id: int,
):
    product = product_service.get_instance_by_user(id, active_user)
    product_service.delete(product.id)
