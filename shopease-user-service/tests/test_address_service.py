import pytest

from fastapi import HTTPException

from app.models.user_model import User
from app.models.address_model import Address
from app.schemas.address_schema import AddressCreate, AddressUpdate

from app.services.address_service import (
    create_address,
    get_addresses,
    get_address,
    update_address,
    delete_address,
    set_default_address
)


def make_address(city="Coimbatore", is_default=False):
    return AddressCreate(
        address_type="HOME",
        full_name="Test User",
        phone_number="+919876543210",
        address_line_1="123 Main Road",
        address_line_2=None,
        city=city,
        state="Tamil Nadu",
        country="India",
        postal_code="641001",
        is_default=is_default
    )


def test_first_address_becomes_default(db):
    address = create_address(db, 1001, make_address())

    assert address.is_default is True


def test_new_default_clears_previous_default(db):
    first = create_address(db, 1001, make_address())

    second = create_address(
        db, 1001, make_address("Chennai", True)
    )

    db.refresh(first)

    assert first.is_default is False
    assert second.is_default is True


def test_set_default_address(db):
    first = create_address(db, 1001, make_address())
    second = create_address(db, 1001, make_address("Chennai"))

    updated = set_default_address(db, 1001, second.id)

    db.refresh(first)

    assert updated.is_default is True
    assert first.is_default is False


def test_unsetting_default_promotes_another_address(db):
    first = create_address(db, 1001, make_address())
    second = create_address(db, 1001, make_address("Chennai", True))

    updated = update_address(
        db,
        1001,
        second.id,
        AddressUpdate(is_default=False)
    )

    db.refresh(first)

    assert updated.is_default is False
    assert first.is_default is True


def test_only_default_address_cannot_be_unset(db):
    address = create_address(db, 1001, make_address())

    with pytest.raises(HTTPException) as error:
        update_address(
            db,
            1001,
            address.id,
            AddressUpdate(is_default=False)
        )

    assert error.value.status_code == 400

    db.refresh(address)
    assert address.is_default is True


def test_deleting_default_promotes_oldest_remaining_address(db):
    first = create_address(db, 1001, make_address())
    second = create_address(db, 1001, make_address("Chennai", True))

    delete_address(db, 1001, second.id)

    db.refresh(first)

    assert first.is_default is True
    assert db.query(Address).filter(Address.id == second.id).first() is None


def test_user_cannot_access_another_users_address(db):
    address = create_address(db, 1001, make_address())

    another_user = User(
        auth_user_id=2002,
        full_name="Another User",
        is_active=True
    )

    db.add(another_user)
    db.commit()

    with pytest.raises(HTTPException) as error:
        get_address(db, 2002, address.id)

    assert error.value.status_code == 404


def test_get_addresses_returns_default_first(db):
    first = create_address(db, 1001, make_address())
    second = create_address(db, 1001, make_address("Chennai", True))

    addresses = get_addresses(db, 1001)

    assert addresses[0].id == second.id
    assert addresses[1].id == first.id
