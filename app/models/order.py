from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum as SQLEnum, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.order_status import OrderStatus

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.mountain_model import MountainModel


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("quantity >= 1"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    mountain_model_id: Mapped[int] = mapped_column(
        ForeignKey("mountain_models.id"), index=True
    )
    quantity: Mapped[int]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount_percent: Mapped[int] = mapped_column(server_default="0")
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status"), server_default=OrderStatus.NEW.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    mountain_model: Mapped["MountainModel"] = relationship(back_populates="orders")
