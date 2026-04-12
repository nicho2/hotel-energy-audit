from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.project_template_repository import ProjectTemplateRepository
from app.repositories.reference_data_repository import ReferenceDataRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.reference_data import (
    ProjectTemplateCreate,
    ProjectTemplateResponse,
    ProjectTemplateUpdate,
)
from app.services.project_template_service import ProjectTemplateService

router = APIRouter()


def get_project_template_service(db: Session) -> ProjectTemplateService:
    return ProjectTemplateService(
        ProjectTemplateRepository(db),
        ReferenceDataRepository(db),
    )


@router.get("", response_model=ApiResponse[list[ProjectTemplateResponse]])
def list_project_templates(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ProjectTemplateResponse]]:
    service = get_project_template_service(db)
    return success_response(
        service.list_templates(current_user, include_inactive=include_inactive)
    )


@router.get("/{template_id}", response_model=ApiResponse[ProjectTemplateResponse])
def get_project_template(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectTemplateResponse]:
    service = get_project_template_service(db)
    return success_response(service.get_template(template_id, current_user))


@router.post("", response_model=ApiResponse[ProjectTemplateResponse], status_code=201)
def create_project_template(
    payload: ProjectTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectTemplateResponse]:
    service = get_project_template_service(db)
    return success_response(service.create_template(payload, current_user))


@router.patch("/{template_id}", response_model=ApiResponse[ProjectTemplateResponse])
def update_project_template(
    template_id: UUID,
    payload: ProjectTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectTemplateResponse]:
    service = get_project_template_service(db)
    return success_response(service.update_template(template_id, payload, current_user))


@router.delete("/{template_id}", response_model=ApiResponse[ProjectTemplateResponse])
def deactivate_project_template(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectTemplateResponse]:
    service = get_project_template_service(db)
    return success_response(service.deactivate_template(template_id, current_user))
