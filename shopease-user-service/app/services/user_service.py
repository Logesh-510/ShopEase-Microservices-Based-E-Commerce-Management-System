from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schema import (
    UserProfileCreate,
    UserProfileUpdate
)


def create_user_profile(
    db: Session,
    auth_user_id: int,
    profile_data: UserProfileCreate
):
    existing_profile = (
        db.query(User)
        .filter(User.auth_user_id == auth_user_id)
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User profile already exists"
        )

    profile = User(
        auth_user_id=auth_user_id,
        **profile_data.model_dump()
    )

    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    except Exception:
        db.rollback()
        raise


def get_user_profile(db: Session, auth_user_id: int):
    profile = (
        db.query(User)
        .filter(User.auth_user_id == auth_user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    if not profile.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User profile is deactivated"
        )

    return profile


def update_user_profile(
    db: Session,
    auth_user_id: int,
    profile_data: UserProfileUpdate
):
    profile = get_user_profile(db, auth_user_id)

    update_data = profile_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(profile, field, value)

    try:
        db.commit()
        db.refresh(profile)
        return profile
    except Exception:
        db.rollback()
        raise


def deactivate_user_profile(db: Session, auth_user_id: int):
    profile = get_user_profile(db, auth_user_id)

    profile.is_active = False

    try:
        db.commit()
        db.refresh(profile)
        return profile
    except Exception:
        db.rollback()
        raise
