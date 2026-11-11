from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_auth_user
from app.database.connection import get_db

from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse
)

from app.services import address_service


router = APIRouter(
    prefix="/api/v1/users/addresses",
    tags=["User Addresses"]
)


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED
)
def create_address(
    address_data: AddressCreate,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.create_address(
        db,
        current_user["user_id"],
        address_data
    )


@router.get(
    "",
    response_model=list[AddressResponse]
)
def get_addresses(
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.get_addresses(
        db,
        current_user["user_id"]
    )


@router.get(
    "/{address_id}",
    response_model=AddressResponse
)
def get_address(
    address_id: int,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.get_address(
        db,
        current_user["user_id"],
        address_id
    )


@router.put(
    "/{address_id}",
    response_model=AddressResponse
)
def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.update_address(
        db,
        current_user["user_id"],
        address_id,
        address_data
    )


@router.delete(
    "/{address_id}"
)
def delete_address(
    address_id: int,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.delete_address(
        db,
        current_user["user_id"],
        address_id
    )


@router.patch(
    "/{address_id}/default",
    response_model=AddressResponse
)
def set_default_address(
    address_id: int,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return address_service.set_default_address(
        db,
        current_user["user_id"],
        address_id
    )
