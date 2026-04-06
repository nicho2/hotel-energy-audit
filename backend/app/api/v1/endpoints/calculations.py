from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.calculation.engine import CalculationEngine
from app.db.models.user import User
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.results_repository import ResultsRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.calculations import CalculationResultLatestResponse
from app.schemas.common import ApiResponse, success_response
from app.schemas.readiness import CalculationReadinessResponse
from app.services.calculation_service import CalculationService
from app.services.project_service import ProjectService
from app.services.readiness_service import ReadinessService
from app.services.results_service import ResultsService

router = APIRouter()


def get_readiness_service(db: Session) -> ReadinessService:
    project_service = ProjectService(ProjectRepository(db))
    return ReadinessService(
        project_service=project_service,
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        technical_system_repository=TechnicalSystemRepository(db),
    )


def get_calculation_service(db: Session) -> CalculationService:
    project_service = ProjectService(ProjectRepository(db))
    readiness_service = ReadinessService(
        project_service=project_service,
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        technical_system_repository=TechnicalSystemRepository(db),
    )
    return CalculationService(
        project_service=project_service,
        scenario_repository=ScenarioRepository(db),
        calculation_repository=CalculationRepository(db),
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        technical_system_repository=TechnicalSystemRepository(db),
        bacs_repository=BacsRepository(db),
        readiness_service=readiness_service,
        engine=CalculationEngine(),
    )


def get_results_service(db: Session) -> ResultsService:
    project_service = ProjectService(ProjectRepository(db))
    return ResultsService(
        project_service=project_service,
        scenario_repository=ScenarioRepository(db),
        results_repository=ResultsRepository(db),
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


@router.post(
    "/{project_id}/scenarios/{scenario_id}/calculate",
    response_model=ApiResponse[CalculationResultLatestResponse],
)
def calculate_scenario(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[CalculationResultLatestResponse]:
    service = get_calculation_service(db)
    return success_response(service.calculate(project_id, scenario_id, current_user))


@router.get(
    "/{project_id}/scenarios/{scenario_id}/results/latest",
    response_model=ApiResponse[CalculationResultLatestResponse],
)
def get_latest_result(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[CalculationResultLatestResponse]:
    service = get_results_service(db)
    return success_response(service.get_latest_result(project_id, scenario_id, current_user))
