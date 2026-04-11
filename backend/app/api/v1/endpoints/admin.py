from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    AdminBrandingProfileCreate,
    AdminBrandingProfileUpdate,
    AdminUserCreate,
    AdminUserResponse,
)
from app.schemas.branding import BrandingProfileResponse
from app.schemas.common import ApiResponse, success_response
from app.services.admin_service import AdminService

router = APIRouter()


def get_admin_service(db: Session) -> AdminService:
    return AdminService(UserRepository(db), BrandingRepository(db))


@router.get("/users", response_model=ApiResponse[list[AdminUserResponse]])
def list_admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[AdminUserResponse]]:
    service = get_admin_service(db)
    data = [AdminUserResponse.model_validate(user) for user in service.list_users(current_user)]
    return success_response(data)


@router.post("/users", response_model=ApiResponse[AdminUserResponse])
def create_admin_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AdminUserResponse]:
    service = get_admin_service(db)
    return success_response(AdminUserResponse.model_validate(service.create_user(payload, current_user)))


@router.post("/users/{user_id}/deactivate", response_model=ApiResponse[AdminUserResponse])
def deactivate_admin_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AdminUserResponse]:
    service = get_admin_service(db)
    return success_response(AdminUserResponse.model_validate(service.deactivate_user(user_id, current_user)))


@router.get("/branding", response_model=ApiResponse[list[BrandingProfileResponse]])
def list_admin_branding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[BrandingProfileResponse]]:
    service = get_admin_service(db)
    data = [BrandingProfileResponse.model_validate(profile) for profile in service.list_branding_profiles(current_user)]
    return success_response(data)


@router.post("/branding", response_model=ApiResponse[BrandingProfileResponse])
def create_admin_branding(
    payload: AdminBrandingProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BrandingProfileResponse]:
    service = get_admin_service(db)
    return success_response(BrandingProfileResponse.model_validate(service.create_branding_profile(payload, current_user)))


@router.patch("/branding/{profile_id}", response_model=ApiResponse[BrandingProfileResponse])
def update_admin_branding(
    profile_id: UUID,
    payload: AdminBrandingProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BrandingProfileResponse]:
    service = get_admin_service(db)
    return success_response(BrandingProfileResponse.model_validate(service.update_branding_profile(profile_id, payload, current_user)))
