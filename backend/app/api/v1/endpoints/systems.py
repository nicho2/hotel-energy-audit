from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.systems import (
    TechnicalSystemCreate,
    TechnicalSystemResponse,
    TechnicalSystemUpdate,
)
from app.services.project_service import ProjectService
from app.services.technical_system_service import TechnicalSystemService

router = APIRouter()


def get_technical_system_service(db: Session) -> TechnicalSystemService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    return TechnicalSystemService(TechnicalSystemRepository(db), project_service)


@router.get("/{project_id}/systems", response_model=ApiResponse[list[TechnicalSystemResponse]])
def list_systems(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[TechnicalSystemResponse]]:
    service = get_technical_system_service(db)
    systems = service.list_systems(project_id, current_user)
    return success_response([TechnicalSystemResponse.model_validate(system) for system in systems])


@router.post("/{project_id}/systems", response_model=ApiResponse[TechnicalSystemResponse])
def create_system(
    project_id: UUID,
    payload: TechnicalSystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[TechnicalSystemResponse]:
    service = get_technical_system_service(db)
    system = service.create_system(project_id, payload, current_user)
    return success_response(TechnicalSystemResponse.model_validate(system))


@router.patch("/{project_id}/systems/{system_id}", response_model=ApiResponse[TechnicalSystemResponse])
def update_system(
    project_id: UUID,
    system_id: UUID,
    payload: TechnicalSystemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[TechnicalSystemResponse]:
    service = get_technical_system_service(db)
    system = service.update_system(project_id, system_id, payload, current_user)
    return success_response(TechnicalSystemResponse.model_validate(system))


@router.delete("/{project_id}/systems/{system_id}", response_model=ApiResponse[TechnicalSystemResponse])
def delete_system(
    project_id: UUID,
    system_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[TechnicalSystemResponse]:
    service = get_technical_system_service(db)
    system = service.delete_system(project_id, system_id, current_user)
    return success_response(TechnicalSystemResponse.model_validate(system))
