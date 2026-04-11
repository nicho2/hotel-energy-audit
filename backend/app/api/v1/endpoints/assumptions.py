from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.assumptions import ProjectAssumptionsResponse
from app.schemas.common import ApiResponse, success_response
from app.services.assumptions_service import AssumptionsService

router = APIRouter()


def get_assumptions_service(db: Session) -> AssumptionsService:
    return AssumptionsService(
        project_repository=ProjectRepository(db),
        building_repository=BuildingRepository(db),
        bacs_repository=BacsRepository(db),
        calculation_repository=CalculationRepository(db),
    )


@router.get(
    "/{project_id}/assumptions",
    response_model=ApiResponse[ProjectAssumptionsResponse],
)
def get_project_assumptions(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectAssumptionsResponse]:
    service = get_assumptions_service(db)
    return success_response(service.get_project_assumptions(project_id, current_user))
