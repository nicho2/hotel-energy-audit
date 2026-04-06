from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.results_repository import ResultsRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.results import ResultsByUseResponse, ResultsByZoneResponse
from app.services.project_service import ProjectService
from app.services.results_service import ResultsService

router = APIRouter()


def get_results_service(db: Session) -> ResultsService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return ResultsService(
        project_service=project_service,
        scenario_repository=ScenarioRepository(db),
        results_repository=ResultsRepository(db),
        technical_system_repository=TechnicalSystemRepository(db),
    )


@router.get(
    "/projects/{project_id}/scenarios/{scenario_id}/results/by-use",
    response_model=ApiResponse[ResultsByUseResponse],
)
def get_results_by_use(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ResultsByUseResponse]:
    service = get_results_service(db)
    return success_response(service.get_results_by_use(project_id, scenario_id, current_user))


@router.get(
    "/projects/{project_id}/scenarios/{scenario_id}/results/by-zone",
    response_model=ApiResponse[ResultsByZoneResponse],
)
def get_results_by_zone(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ResultsByZoneResponse]:
    service = get_results_service(db)
    return success_response(service.get_results_by_zone(project_id, scenario_id, current_user))
