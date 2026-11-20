from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Numeric, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.order import Order


class MountainModel(Base):
    __tablename__ = "mountain_models"
    __table_args__ = (
        CheckConstraint("price > 0"),
        CheckConstraint("stock_quantity >= 0"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    mountain_range: Mapped[str] = mapped_column(String(120))
    scale: Mapped[str] = mapped_column(String(32))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock_quantity: Mapped[int]
    is_active: Mapped[bool] = mapped_column(server_default=true())

    orders: Mapped[list["Order"]] = relationship(
        back_populates="mountain_model", passive_deletes="all"
    )
