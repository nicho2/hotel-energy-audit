from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.projects import ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("", response_model=ApiResponse[list[ProjectResponse]])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ProjectResponse]]:
    service = ProjectService(ProjectRepository(db))
    projects = service.list_projects(current_user)
    data = [ProjectResponse.model_validate(project) for project in projects]
    return success_response(data)
