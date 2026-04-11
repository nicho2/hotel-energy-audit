from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.audit_repository import AuditRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.history import ProjectHistoryEventResponse
from app.services.history_service import HistoryService

router = APIRouter()


def get_history_service(db: Session) -> HistoryService:
    return HistoryService(ProjectRepository(db), HistoryRepository(db), AuditRepository(db))


@router.get(
    "/{project_id}/history",
    response_model=ApiResponse[list[ProjectHistoryEventResponse]],
)
def list_project_history(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ProjectHistoryEventResponse]]:
    service = get_history_service(db)
    return success_response(service.list_project_history(project_id, current_user))


@router.get(
    "/{project_id}/scenarios/{scenario_id}/history",
    response_model=ApiResponse[list[ProjectHistoryEventResponse]],
)
def list_scenario_history(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ProjectHistoryEventResponse]]:
    service = get_history_service(db)
    return success_response(service.list_scenario_history(project_id, scenario_id, current_user))
