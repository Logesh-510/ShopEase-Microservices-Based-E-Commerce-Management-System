from datetime import datetime
import re
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)


AddressType = Literal["HOME", "WORK", "OTHER"]


def validate_phone(value: str) -> str:
    value = value.strip()

    if not re.fullmatch(r"\+?[0-9\s()\-]+", value):
        raise ValueError("Phone number contains invalid characters")

    digits = re.sub(r"[\s()\-]", "", value).lstrip("+")

    if not 8 <= len(digits) <= 15:
        raise ValueError("Phone number must contain 8 to 15 digits")

    return value


class AddressCreate(BaseModel):
    address_type: AddressType
    full_name: str = Field(min_length=2, max_length=150)
    phone_number: str = Field(min_length=8, max_length=20)

    address_line_1: str = Field(min_length=3, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)

    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(min_length=3, max_length=20)

    is_default: bool = False

    @field_validator(
        "full_name",
        "address_line_1",
        "city",
        "state",
        "country",
        "postal_code"
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        return validate_phone(value)

    @field_validator("address_line_2")
    @classmethod
    def normalize_address_line_2(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            return value or None

        return None


class AddressUpdate(BaseModel):
    address_type: AddressType | None = None
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, min_length=8, max_length=20)

    address_line_1: str | None = Field(default=None, min_length=3, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)

    city: str | None = Field(default=None, min_length=2, max_length=100)
    state: str | None = Field(default=None, min_length=2, max_length=100)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=3, max_length=20)

    is_default: bool | None = None

    @model_validator(mode="after")
    def validate_non_empty_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one address field must be provided")

        return self

    @field_validator(
        "address_type",
        "full_name",
        "phone_number",
        "address_line_1",
        "city",
        "state",
        "country",
        "postal_code",
        "is_default",
        mode="before"
    )
    @classmethod
    def reject_null_required_updates(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")

        return value

    @field_validator(
        "full_name",
        "address_line_1",
        "city",
        "state",
        "country",
        "postal_code"
    )
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_optional_phone(cls, value: str | None) -> str | None:
        return validate_phone(value)

    @field_validator("address_line_2")
    @classmethod
    def normalize_optional_address_line_2(
        cls,
        value: str | None
    ) -> str | None:
        if value is not None:
            value = value.strip()
            return value or None

        return None


class AddressResponse(BaseModel):
    id: int
    user_id: int
    address_type: str
    full_name: str
    phone_number: str
    address_line_1: str
    address_line_2: str | None
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
