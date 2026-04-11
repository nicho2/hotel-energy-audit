from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.assumption_set_repository import AssumptionSetRepository
from app.repositories.branding_repository import BrandingRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    AdminBrandingProfileCreate,
    AdminBrandingProfileUpdate,
    AdminUserCreate,
    AdminUserResponse,
)
from app.schemas.assumption_sets import (
    AssumptionSetCloneRequest,
    AssumptionSetCreate,
    AssumptionSetResponse,
    AssumptionSetUpdate,
)
from app.schemas.branding import BrandingProfileResponse
from app.schemas.common import ApiResponse, success_response
from app.services.assumption_set_service import AssumptionSetService
from app.services.admin_service import AdminService

router = APIRouter()


def get_admin_service(db: Session) -> AdminService:
    return AdminService(UserRepository(db), BrandingRepository(db))


def get_assumption_set_service(db: Session) -> AssumptionSetService:
    return AssumptionSetService(AssumptionSetRepository(db))


@router.get("/users", response_model=ApiResponse[list[AdminUserResponse]])
def list_admin_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[AdminUserResponse]]:
    service = get_admin_service(db)
    data = [
        AdminUserResponse.model_validate(user)
        for user in service.list_users(current_user)
    ]
    return success_response(data)


@router.post("/users", response_model=ApiResponse[AdminUserResponse])
def create_admin_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AdminUserResponse]:
    service = get_admin_service(db)
    return success_response(
        AdminUserResponse.model_validate(service.create_user(payload, current_user))
    )


@router.post("/users/{user_id}/deactivate", response_model=ApiResponse[AdminUserResponse])
def deactivate_admin_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AdminUserResponse]:
    service = get_admin_service(db)
    return success_response(
        AdminUserResponse.model_validate(service.deactivate_user(user_id, current_user))
    )


@router.get("/branding", response_model=ApiResponse[list[BrandingProfileResponse]])
def list_admin_branding(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[BrandingProfileResponse]]:
    service = get_admin_service(db)
    data = [
        BrandingProfileResponse.model_validate(profile)
        for profile in service.list_branding_profiles(current_user)
    ]
    return success_response(data)


@router.post("/branding", response_model=ApiResponse[BrandingProfileResponse])
def create_admin_branding(
    payload: AdminBrandingProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BrandingProfileResponse]:
    service = get_admin_service(db)
    return success_response(
        BrandingProfileResponse.model_validate(
            service.create_branding_profile(payload, current_user)
        )
    )


@router.patch("/branding/{profile_id}", response_model=ApiResponse[BrandingProfileResponse])
def update_admin_branding(
    profile_id: UUID,
    payload: AdminBrandingProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BrandingProfileResponse]:
    service = get_admin_service(db)
    return success_response(
        BrandingProfileResponse.model_validate(
            service.update_branding_profile(profile_id, payload, current_user)
        )
    )


@router.get("/assumption-sets", response_model=ApiResponse[list[AssumptionSetResponse]])
def list_admin_assumption_sets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[AssumptionSetResponse]]:
    service = get_assumption_set_service(db)
    return success_response(service.list_assumption_sets(current_user))


@router.get(
    "/assumption-sets/{assumption_set_id}",
    response_model=ApiResponse[AssumptionSetResponse],
)
def get_admin_assumption_set(
    assumption_set_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.get_assumption_set(assumption_set_id, current_user))


@router.post(
    "/assumption-sets",
    response_model=ApiResponse[AssumptionSetResponse],
    status_code=201,
)
def create_admin_assumption_set(
    payload: AssumptionSetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.create_assumption_set(payload, current_user))


@router.patch(
    "/assumption-sets/{assumption_set_id}",
    response_model=ApiResponse[AssumptionSetResponse],
)
def update_admin_assumption_set(
    assumption_set_id: UUID,
    payload: AssumptionSetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.update_assumption_set(assumption_set_id, payload, current_user))


@router.post(
    "/assumption-sets/{assumption_set_id}/clone",
    response_model=ApiResponse[AssumptionSetResponse],
    status_code=201,
)
def clone_admin_assumption_set(
    assumption_set_id: UUID,
    payload: AssumptionSetCloneRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.clone_assumption_set(assumption_set_id, payload, current_user))


@router.post(
    "/assumption-sets/{assumption_set_id}/activate",
    response_model=ApiResponse[AssumptionSetResponse],
)
def activate_admin_assumption_set(
    assumption_set_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.activate_assumption_set(assumption_set_id, current_user))


@router.post(
    "/assumption-sets/{assumption_set_id}/deactivate",
    response_model=ApiResponse[AssumptionSetResponse],
)
def deactivate_admin_assumption_set(
    assumption_set_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[AssumptionSetResponse]:
    service = get_assumption_set_service(db)
    return success_response(service.deactivate_assumption_set(assumption_set_id, current_user))
