from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.buildings import BuildingResponse, BuildingUpsert
from app.schemas.common import ApiResponse, success_response
from app.services.building_service import BuildingService
from app.services.project_service import ProjectService

router = APIRouter()


def get_building_service(db: Session) -> BuildingService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return BuildingService(BuildingRepository(db), project_service)


@router.get("/{project_id}/building", response_model=ApiResponse[BuildingResponse | None])
def get_building(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BuildingResponse | None]:
    service = get_building_service(db)
    building = service.get_building(project_id, current_user)
    data = BuildingResponse.model_validate(building) if building is not None else None
    return success_response(data)


@router.put("/{project_id}/building", response_model=ApiResponse[BuildingResponse])
def put_building(
    project_id: UUID,
    payload: BuildingUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BuildingResponse]:
    service = get_building_service(db)
    building = service.upsert_building(project_id, payload, current_user)
    return success_response(BuildingResponse.model_validate(building))
