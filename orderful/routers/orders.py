from typing import Annotated

from fastapi import APIRouter, Depends, status

from orderful.core.settings import settings
from orderful.models.associations import OrderProductAssociation
from orderful.models.users import User
from orderful.schemas import orders as schemas
from orderful.services.orders import OrderService, order_service
from orderful.services.products import ProductService, product_service
from orderful.services.users import get_current_active_user

router = APIRouter(prefix="/orders")


@router.get("/", response_model=list[schemas.Order])
def get_orders(
    active_user: Annotated[User, Depends(get_current_active_user)],
    order_service: Annotated[OrderService, Depends(order_service)],
    offset: int = settings.OFFSET,
    limit: int = settings.LIMIT,
):
    return order_service.get_instances_by_user(offset, limit, active_user)


@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(
    active_user: Annotated[User, Depends(get_current_active_user)],
    order_service: Annotated[OrderService, Depends(order_service)],
    product_service: Annotated[ProductService, Depends(product_service)],
    data: schemas.CreateOrder,
):
    return order_service.save_with_associations(
        data,
        "product_id",
        "products",
        "order",
        product_service,
        OrderProductAssociation,
        user_id=active_user.id,
    )


@router.get("/{id}", response_model=schemas.Order)
def get_order(
    active_user: Annotated[User, Depends(get_current_active_user)],
    order_service: Annotated[OrderService, Depends(order_service)],
    id: int,
):
    return order_service.get_instance_by_user(id, active_user)


@router.put("/{id}", response_model=schemas.Order)
def update_order(
    active_user: Annotated[User, Depends(get_current_active_user)],
    order_service: Annotated[OrderService, Depends(order_service)],
    data: schemas.UpdateOrder,
    id: int,
):
    order = order_service.get_instance_by_user(id, active_user)
    return order_service.update(order, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    active_user: Annotated[User, Depends(get_current_active_user)],
    order_service: Annotated[OrderService, Depends(order_service)],
    id: int,
):
    order = order_service.get_instance_by_user(id, active_user)
    order_service.delete(order.id)
