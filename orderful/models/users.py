from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from orderful.models.base import AuditDatesMixin, Base


class User(AuditDatesMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    superuser: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=False)
