from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.assumption_set_repository import AssumptionSetRepository
from app.repositories.branding_repository import BrandingRepository
from app.repositories.solution_catalog_repository import SolutionCatalogRepository
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
from app.schemas.solutions import (
    SolutionCatalogResponse,
    SolutionDefinitionCreate,
    SolutionDefinitionResponse,
    SolutionDefinitionUpdate,
)
from app.services.assumption_set_service import AssumptionSetService
from app.services.admin_service import AdminService
from app.services.solution_catalog_service import SolutionCatalogService

router = APIRouter()


def get_admin_service(db: Session) -> AdminService:
    return AdminService(UserRepository(db), BrandingRepository(db))


def get_assumption_set_service(db: Session) -> AssumptionSetService:
    return AssumptionSetService(AssumptionSetRepository(db))


def get_solution_catalog_service(db: Session) -> SolutionCatalogService:
    return SolutionCatalogService(SolutionCatalogRepository(db))


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


@router.get("/solution-catalogs", response_model=ApiResponse[list[SolutionCatalogResponse]])
def list_admin_solution_catalogs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[SolutionCatalogResponse]]:
    service = get_solution_catalog_service(db)
    service.ensure_admin(current_user)
    return success_response(service.list_catalogs(current_user))


@router.get("/solutions", response_model=ApiResponse[list[SolutionDefinitionResponse]])
def list_admin_solutions(
    country: str | None = None,
    family: str | None = None,
    building_type: str | None = None,
    zone_type: str | None = None,
    scope: str | None = None,
    include_inactive: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[SolutionDefinitionResponse]]:
    service = get_solution_catalog_service(db)
    service.ensure_admin(current_user)
    return success_response(
        service.list_solutions(
            current_user,
            country=country,
            family=family,
            building_type=building_type,
            zone_type=zone_type,
            scope=scope,
            include_inactive=include_inactive,
        )
    )


@router.post("/solutions", response_model=ApiResponse[SolutionDefinitionResponse], status_code=201)
def create_admin_solution(
    payload: SolutionDefinitionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[SolutionDefinitionResponse]:
    service = get_solution_catalog_service(db)
    return success_response(service.create_solution(payload, current_user))


@router.patch("/solutions/{solution_id}", response_model=ApiResponse[SolutionDefinitionResponse])
def update_admin_solution(
    solution_id: UUID,
    payload: SolutionDefinitionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[SolutionDefinitionResponse]:
    service = get_solution_catalog_service(db)
    return success_response(service.update_solution(solution_id, payload, current_user))


@router.post("/solutions/{solution_id}/deactivate", response_model=ApiResponse[SolutionDefinitionResponse])
def deactivate_admin_solution(
    solution_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[SolutionDefinitionResponse]:
    service = get_solution_catalog_service(db)
    return success_response(service.deactivate_solution(solution_id, current_user))
