from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MountainModelWrite(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    mountain_range: str = Field(min_length=1, max_length=120)
    scale: str = Field(min_length=1, max_length=32)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(ge=0, le=2_147_483_647)
    is_active: bool = True


class MountainModelRead(MountainModelWrite):
    model_config = ConfigDict(from_attributes=True)

    id: int
