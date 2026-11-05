from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    FiniteFloat,
    StrictInt
)


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    price: FiniteFloat = Field(..., gt=0)
    stock_quantity: StrictInt = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    status: Literal["Active", "Inactive"] = "Active"

    @field_validator("name", "category")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot contain only spaces")

        return value


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    price: FiniteFloat | None = Field(default=None, gt=0)
    stock_quantity: StrictInt | None = Field(default=None, ge=0)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    status: Literal["Active", "Inactive"] | None = None

    @field_validator("name", "category")
    @classmethod
    def validate_text(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("This field cannot contain only spaces")

        return value


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: float
    stock_quantity: int
    category: str
    status: Literal["Active", "Inactive"]
    created_at: datetime
