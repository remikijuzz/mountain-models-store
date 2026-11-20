from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.order_status import OrderStatus


class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: int = Field(ge=1, le=2_147_483_647)
    mountain_model_id: int = Field(ge=1, le=2_147_483_647)
    quantity: int = Field(ge=1, le=2_147_483_647)


class OrderStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: OrderStatus


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    mountain_model_id: int
    quantity: int
    unit_price: Decimal
    discount_percent: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
