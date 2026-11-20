from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerWrite(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr


class CustomerRead(CustomerWrite):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
