from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.bacs_repository import BacsRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.bacs import (
    BacsAssessmentUpsert,
    BacsCurrentFunctionsUpdate,
    BacsCurrentResponse,
    BacsSummaryResponse,
)
from app.schemas.common import ApiResponse, success_response
from app.services.bacs_service import BacsService
from app.services.project_service import ProjectService

router = APIRouter()


def get_bacs_service(db: Session) -> BacsService:
    project_service = ProjectService(ProjectRepository(db))
    return BacsService(BacsRepository(db), project_service)


@router.get("/{project_id}/bacs/current", response_model=ApiResponse[BacsCurrentResponse])
def get_current_bacs(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BacsCurrentResponse]:
    service = get_bacs_service(db)
    return success_response(service.get_current_assessment(project_id, current_user))


@router.post("/{project_id}/bacs/current", response_model=ApiResponse[BacsCurrentResponse])
def post_current_bacs(
    project_id: UUID,
    payload: BacsAssessmentUpsert,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BacsCurrentResponse]:
    service = get_bacs_service(db)
    return success_response(service.upsert_current_assessment(project_id, payload, current_user))


@router.put("/{project_id}/bacs/current/functions", response_model=ApiResponse[BacsCurrentResponse])
def put_current_bacs_functions(
    project_id: UUID,
    payload: BacsCurrentFunctionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BacsCurrentResponse]:
    service = get_bacs_service(db)
    return success_response(service.replace_current_functions(project_id, payload, current_user))


@router.get("/{project_id}/bacs/current/summary", response_model=ApiResponse[BacsSummaryResponse])
def get_current_bacs_summary(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[BacsSummaryResponse]:
    service = get_bacs_service(db)
    return success_response(service.get_current_summary(project_id, current_user))
