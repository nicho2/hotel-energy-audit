from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.wizard import WizardStateResponse
from app.services.project_service import ProjectService
from app.services.wizard_service import WizardService

router = APIRouter()


def get_wizard_service(db: Session) -> WizardService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return WizardService(project_service)


@router.get("/{project_id}/wizard", response_model=ApiResponse[WizardStateResponse])
def get_wizard_state(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[WizardStateResponse]:
    service = get_wizard_service(db)
    return success_response(service.get_wizard_state(project_id, current_user))
