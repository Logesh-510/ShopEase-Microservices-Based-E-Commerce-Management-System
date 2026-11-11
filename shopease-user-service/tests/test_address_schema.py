import pytest
from pydantic import ValidationError

from app.schemas.address_schema import AddressCreate, AddressUpdate


VALID_ADDRESS = {
    "address_type": "HOME",
    "full_name": "Logesh Sakthivel",
    "phone_number": "+919876543210",
    "address_line_1": "123 Main Road",
    "address_line_2": "Near Bus Stand",
    "city": "Coimbatore",
    "state": "Tamil Nadu",
    "country": "India",
    "postal_code": "641001",
    "is_default": False,
}


def test_valid_address_creation():
    address = AddressCreate(**VALID_ADDRESS)
    assert address.city == "Coimbatore"
    assert address.is_default is False


def test_first_address_default_field_defaults_to_false():
    data = VALID_ADDRESS.copy()
    data.pop("is_default")
    address = AddressCreate(**data)
    assert address.is_default is False


@pytest.mark.parametrize("phone", [
    "++9876543211",
    "abcdefghij",
    "12345",
])
def test_invalid_phone_numbers_rejected(phone):
    data = VALID_ADDRESS.copy()
    data["phone_number"] = phone

    with pytest.raises(ValidationError):
        AddressCreate(**data)


def test_empty_required_name_rejected():
    data = VALID_ADDRESS.copy()
    data["full_name"] = "   "

    with pytest.raises(ValidationError):
        AddressCreate(**data)


def test_empty_update_rejected():
    with pytest.raises(ValidationError):
        AddressUpdate()


def test_null_required_update_rejected():
    with pytest.raises(ValidationError):
        AddressUpdate(full_name=None)


def test_null_is_default_rejected():
    with pytest.raises(ValidationError):
        AddressUpdate(is_default=None)


def test_invalid_update_phone_rejected():
    with pytest.raises(ValidationError):
        AddressUpdate(phone_number="++9876543211")


def test_optional_address_line_can_be_cleared():
    update = AddressUpdate(address_line_2=None)
    assert update.address_line_2 is None


def test_valid_partial_update():
    update = AddressUpdate(city="Chennai")
    assert update.city == "Chennai"
    assert update.model_fields_set == {"city"}


def test_valid_default_address_update():
    update = AddressUpdate(is_default=True)
    assert update.is_default is True
