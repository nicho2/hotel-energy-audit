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
from app.schemas.scenario_comparison import ScenarioComparisonRequest, ScenarioComparisonResponse
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


@router.post(
    "/{project_id}/scenarios/compare",
    response_model=ApiResponse[ScenarioComparisonResponse],
)
def compare_scenarios(
    project_id: UUID,
    payload: ScenarioComparisonRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioComparisonResponse]:
    service = get_results_service(db)
    return success_response(service.compare_scenarios(project_id, payload.scenario_ids, current_user))
