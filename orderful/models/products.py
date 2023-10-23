from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orderful.models.base import AuditDatesMixin, Base

if TYPE_CHECKING:
    from .associations import CategoryProductAssociation, OrderProductAssociation
    from .users import User


class Product(AuditDatesMixin, Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    article: Mapped[str] = mapped_column(String(75), unique=True)
    quantity: Mapped[int] = mapped_column()

    orders: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="product")

    categories: Mapped[list["CategoryProductAssociation"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship()
