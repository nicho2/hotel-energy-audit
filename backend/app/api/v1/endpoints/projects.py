from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_project_access
from app.api.deps.db import get_db
from app.db.models.project import Project
from app.db.models.user import User
from app.repositories.audit_repository import AuditRepository
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.audit_service import AuditService
from app.services.project_service import ProjectService

router = APIRouter()


def get_project_service(db: Session) -> ProjectService:
    return ProjectService(
        ProjectRepository(db),
        BrandingRepository(db),
        AuditService(AuditRepository(db)),
    )


@router.get("", response_model=ApiResponse[list[ProjectResponse]])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ProjectResponse]]:
    service = get_project_service(db)
    projects = service.list_projects(current_user)
    data = [ProjectResponse.model_validate(project) for project in projects]
    return success_response(data)


@router.post("", response_model=ApiResponse[ProjectResponse])
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectResponse]:
    service = get_project_service(db)
    project = service.create_project(payload, current_user)
    return success_response(ProjectResponse.model_validate(project))


@router.get("/{project_id}", response_model=ApiResponse[ProjectResponse])
def get_project(
    project_id: UUID,
    _project_access: Project = Depends(require_project_access),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectResponse]:
    service = get_project_service(db)
    project = service.get_project(project_id, current_user)
    return success_response(ProjectResponse.model_validate(project))


@router.patch("/{project_id}", response_model=ApiResponse[ProjectResponse])
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    _project_access: Project = Depends(require_project_access),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ProjectResponse]:
    service = get_project_service(db)
    project = service.update_project(project_id, payload, current_user)
    return success_response(ProjectResponse.model_validate(project))
