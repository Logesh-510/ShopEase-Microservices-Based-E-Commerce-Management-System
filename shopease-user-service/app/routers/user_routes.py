from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import get_current_auth_user
from app.database.connection import get_db

from app.schemas.user_schema import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse
)

from app.services import user_service


router = APIRouter(
    prefix="/api/v1/users",
    tags=["User Profiles"]
)


@router.post(
    "/profile",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    profile_data: UserProfileCreate,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return user_service.create_user_profile(
        db,
        current_user["user_id"],
        profile_data
    )


@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_profile(
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return user_service.get_user_profile(
        db,
        current_user["user_id"]
    )


@router.put(
    "/profile",
    response_model=UserProfileResponse
)
def update_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return user_service.update_user_profile(
        db,
        current_user["user_id"],
        profile_data
    )


@router.patch(
    "/profile/deactivate",
    response_model=UserProfileResponse
)
def deactivate_profile(
    current_user: dict = Depends(get_current_auth_user),
    db: Session = Depends(get_db)
):
    return user_service.deactivate_user_profile(
        db,
        current_user["user_id"]
    )
