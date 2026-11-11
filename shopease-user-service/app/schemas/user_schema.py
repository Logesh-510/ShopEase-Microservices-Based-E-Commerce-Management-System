from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)


class UserProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    profile_image: str | None = Field(default=None, max_length=500)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Full name must contain at least 2 characters")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if value and not value.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
                raise ValueError("Phone number contains invalid characters")
        return value or None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date | None) -> date | None:
        if value is not None and value >= date.today():
            raise ValueError("Date of birth must be in the past")
        return value


class UserProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    profile_image: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_non_empty_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one profile field must be provided")
        return self

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Full name cannot be null")

        value = value.strip()

        if len(value) < 2:
            raise ValueError("Full name must contain at least 2 characters")

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if value and not value.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit():
                raise ValueError("Phone number contains invalid characters")
        return value or None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: date | None) -> date | None:
        if value is not None and value >= date.today():
            raise ValueError("Date of birth must be in the past")
        return value


class UserProfileResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str | None
    date_of_birth: date | None
    gender: str | None
    profile_image: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)