from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orderful.models.base import Base

if TYPE_CHECKING:
    from .orders import Order
    from .products import Product


class OrderProductAssociation(Base):
    __tablename__ = "orders_products_association"

    quantity: Mapped[int] = mapped_column()

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    order: Mapped["Order"] = relationship(back_populates="products")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    product: Mapped["Product"] = relationship(back_populates="orders")


class CategoryProductAssociation(Base):
    __tablename__ = "categories_products_association"

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    product: Mapped["Product"] = relationship(back_populates="categories")
