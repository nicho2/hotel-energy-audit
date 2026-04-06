from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.common import ApiResponse, MetaPayload, success_response
from app.schemas.zones import (
    BuildingZoneCreate,
    BuildingZoneGenerateRequest,
    BuildingZoneResponse,
    BuildingZoneUpdate,
    ZoneValidationResponse,
)
from app.services.project_service import ProjectService
from app.services.zone_service import ZoneService

router = APIRouter()


def get_zone_service(db: Session) -> ZoneService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return ZoneService(ZoneRepository(db), BuildingRepository(db), project_service)


@router.get("/{project_id}/zones", response_model=ApiResponse[list[BuildingZoneResponse]])
def list_zones(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[BuildingZoneResponse]]:
    service = get_zone_service(db)
    zones = service.list_zones(project_id, current_user)
    return success_response([BuildingZoneResponse.model_validate(zone) for zone in zones])


@router.post("/{project_id}/zones", response_model=ApiResponse[BuildingZoneResponse])
def create_zone(
    project_id: UUID,
    payload: BuildingZoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BuildingZoneResponse]:
    service = get_zone_service(db)
    zone = service.create_zone(project_id, payload, current_user)
    return success_response(BuildingZoneResponse.model_validate(zone))


@router.patch("/{project_id}/zones/{zone_id}", response_model=ApiResponse[BuildingZoneResponse])
def update_zone(
    project_id: UUID,
    zone_id: UUID,
    payload: BuildingZoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BuildingZoneResponse]:
    service = get_zone_service(db)
    zone = service.update_zone(project_id, zone_id, payload, current_user)
    return success_response(BuildingZoneResponse.model_validate(zone))


@router.delete("/{project_id}/zones/{zone_id}", response_model=ApiResponse[BuildingZoneResponse])
def delete_zone(
    project_id: UUID,
    zone_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BuildingZoneResponse]:
    service = get_zone_service(db)
    zone = service.delete_zone(project_id, zone_id, current_user)
    return success_response(BuildingZoneResponse.model_validate(zone))


@router.post("/{project_id}/zones/generate", response_model=ApiResponse[list[BuildingZoneResponse]])
def generate_zones(
    project_id: UUID,
    payload: BuildingZoneGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[BuildingZoneResponse]]:
    service = get_zone_service(db)
    result = service.generate_zones(project_id, payload, current_user)
    data = [BuildingZoneResponse.model_validate(zone) for zone in result.zones]
    return success_response(data, meta=MetaPayload(warnings=result.warnings))


@router.get("/{project_id}/zones/validation", response_model=ApiResponse[ZoneValidationResponse])
def validate_zones(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ZoneValidationResponse]:
    service = get_zone_service(db)
    return success_response(service.validate_zones(project_id, current_user))
