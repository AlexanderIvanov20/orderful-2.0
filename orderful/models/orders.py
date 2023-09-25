import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Mapper, mapped_column, object_session, relationship

from orderful.models.base import AuditDatesMixin, Base
from orderful.models.users import User

if TYPE_CHECKING:
    from .associations import OrderProductAssociation


class Order(AuditDatesMixin, Base):
    class Status(enum.Enum):
        PENDING = "PENDING"
        ON_HOLD = "ON_HOLD"
        FAILED = "FAILED"
        IN_PROGRESS = "IN_PROGRESS"
        CANCELLED = "CANCELLED"
        SHIPPED = "SHIPPED"
        RECEIVED = "RECEIVED"
        COMPLETED = "COMPLETED"

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20))
    start_date: Mapped[datetime] = mapped_column()
    status: Mapped[Status] = mapped_column(Enum(Status), server_default=Status.PENDING.value)

    products: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="order")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship()

    @property
    def received(self):
        return self.status == self.Status.RECEIVED


# TODO: Not really logical, managers should confirm an order.
@event.listens_for(Order, "after_insert")
def take_order_in_progress(mapper: Mapper, connection: Connection, target: Order) -> None:
    object_session(target).query(Order).update(
        {
            "status": Order.Status.IN_PROGRESS,
        }
    )


@event.listens_for(Order, "after_update")
def subtract_items_quantity(mapper: Mapper, connection: Connection, target: Order) -> None:
    if (
        target.status == Order.Status.COMPLETED.value
        and target._sa_instance_state.committed_state["status"] != Order.Status.COMPLETED.value
    ):
        for association in target.products:
            association.product.quantity -= association.quantity

        object_session(target).bulk_save_objects(target.products)
