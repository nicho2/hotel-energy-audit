from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.core.exceptions import ValidationError
from app.db.models.user import User
from app.repositories.bacs_repository import BacsRepository
from app.repositories.branding_repository import BrandingRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.scenario_solution_repository import ScenarioSolutionRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.wizard_step_payload_repository import WizardStepPayloadRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.wizard import (
    WizardStateResponse,
    WizardStepSaveRequest,
    WizardStepSaveResponse,
    WizardStepValidationResult,
)
from app.services.project_service import ProjectService
from app.services.wizard_service import WizardService

router = APIRouter()


def get_wizard_service(db: Session) -> WizardService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return WizardService(
        project_service,
        WizardStepPayloadRepository(db),
        BuildingRepository(db),
        ZoneRepository(db),
        TechnicalSystemRepository(db),
        BacsRepository(db),
        ScenarioRepository(db),
        ScenarioSolutionRepository(db),
    )


@router.get("/{project_id}/wizard", response_model=ApiResponse[WizardStateResponse])
def get_wizard_state(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[WizardStateResponse]:
    service = get_wizard_service(db)
    return success_response(service.get_wizard_state(project_id, current_user))


@router.put("/{project_id}/wizard/steps/{step_name}", response_model=ApiResponse[WizardStepSaveResponse])
def save_wizard_step(
    project_id: UUID,
    step_name: str,
    payload: WizardStepSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[WizardStepSaveResponse]:
    service = get_wizard_service(db)
    return success_response(service.save_step(project_id, step_name, payload.payload, current_user))


@router.post("/{project_id}/wizard/steps/{step_name}/validate", response_model=ApiResponse[WizardStepValidationResult])
def validate_wizard_step(
    project_id: UUID,
    step_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[WizardStepValidationResult]:
    service = get_wizard_service(db)
    result = service.validate_step(project_id, step_name, current_user)
    if not result.valid:
        raise ValidationError(
            result.message,
            field=step_name,
            details={
                "step_code": result.step_code,
                "validations": [item.model_dump(mode="json") for item in result.validations],
            },
        )
    return success_response(result)
