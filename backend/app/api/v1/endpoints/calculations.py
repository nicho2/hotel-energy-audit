from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.building_repository import BuildingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.readiness import CalculationReadinessResponse
from app.services.project_service import ProjectService
from app.services.readiness_service import ReadinessService

router = APIRouter()


def get_readiness_service(db: Session) -> ReadinessService:
    project_service = ProjectService(ProjectRepository(db))
    return ReadinessService(
        project_service=project_service,
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        technical_system_repository=TechnicalSystemRepository(db),
    )


@router.get(
    "/{project_id}/calculation-readiness",
    response_model=ApiResponse[CalculationReadinessResponse],
)
def get_calculation_readiness(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[CalculationReadinessResponse]:
    service = get_readiness_service(db)
    return success_response(service.get_calculation_readiness(project_id, current_user))
