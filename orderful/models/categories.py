from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orderful.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    parent: Mapped["Category"] = relationship(back_populates="subcategories", remote_side=[id])
    subcategories: Mapped[list["Category"]] = relationship(back_populates="parent")
