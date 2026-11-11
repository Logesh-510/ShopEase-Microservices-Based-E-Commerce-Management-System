from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.address_model import Address
from app.schemas.address_schema import AddressCreate, AddressUpdate
from app.services.user_service import get_user_profile


def get_address_or_404(db: Session, user_id: int, address_id: int):
    address = (
        db.query(Address)
        .filter(
            Address.id == address_id,
            Address.user_id == user_id
        )
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    return address


def create_address(db: Session, auth_user_id: int, address_data: AddressCreate):
    profile = get_user_profile(db, auth_user_id)

    existing_count = (
        db.query(Address)
        .filter(Address.user_id == profile.id)
        .count()
    )

    data = address_data.model_dump()
    requested_default = data.pop("is_default")

    should_be_default = requested_default or existing_count == 0

    try:
        if should_be_default:
            db.query(Address).filter(
                Address.user_id == profile.id
            ).update(
                {Address.is_default: False},
                synchronize_session=False
            )

        address = Address(
            user_id=profile.id,
            **data,
            is_default=should_be_default
        )

        db.add(address)
        db.commit()
        db.refresh(address)

        return address

    except Exception:
        db.rollback()
        raise


def get_addresses(db: Session, auth_user_id: int):
    profile = get_user_profile(db, auth_user_id)

    return (
        db.query(Address)
        .filter(Address.user_id == profile.id)
        .order_by(Address.is_default.desc(), Address.id.asc())
        .all()
    )


def get_address(db: Session, auth_user_id: int, address_id: int):
    profile = get_user_profile(db, auth_user_id)

    return get_address_or_404(db, profile.id, address_id)


def update_address(
    db: Session,
    auth_user_id: int,
    address_id: int,
    address_data: AddressUpdate
):
    profile = get_user_profile(db, auth_user_id)
    address = get_address_or_404(db, profile.id, address_id)

    update_data = address_data.model_dump(exclude_unset=True)

    try:
        if update_data.get("is_default") is True:
            db.query(Address).filter(
                Address.user_id == profile.id,
                Address.id != address_id
            ).update(
                {Address.is_default: False},
                synchronize_session=False
            )

            address.is_default = True
            update_data.pop("is_default")

        elif update_data.get("is_default") is False and address.is_default:
            next_address = (
                db.query(Address)
                .filter(
                    Address.user_id == profile.id,
                    Address.id != address_id
                )
                .order_by(Address.created_at.asc(), Address.id.asc())
                .first()
            )

            if not next_address:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The only address cannot be unset as default"
                )

            next_address.is_default = True

        for field, value in update_data.items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)

        return address

    except Exception:
        db.rollback()
        raise


def delete_address(db: Session, auth_user_id: int, address_id: int):
    profile = get_user_profile(db, auth_user_id)
    address = get_address_or_404(db, profile.id, address_id)

    try:
        was_default = address.is_default

        db.delete(address)
        db.flush()

        if was_default:
            next_address = (
                db.query(Address)
                .filter(Address.user_id == profile.id)
                .order_by(Address.created_at.asc(), Address.id.asc())
                .first()
            )

            if next_address:
                next_address.is_default = True

        db.commit()

        return {
            "message": "Address deleted successfully",
            "address_id": address_id
        }

    except Exception:
        db.rollback()
        raise


def set_default_address(db: Session, auth_user_id: int, address_id: int):
    profile = get_user_profile(db, auth_user_id)
    address = get_address_or_404(db, profile.id, address_id)

    try:
        db.query(Address).filter(
            Address.user_id == profile.id
        ).update(
            {Address.is_default: False},
            synchronize_session=False
        )

        address.is_default = True

        db.commit()
        db.refresh(address)

        return address

    except Exception:
        db.rollback()
        raise
