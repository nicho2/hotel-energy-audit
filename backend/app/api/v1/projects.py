from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.db import get_db
from app.api.deps.auth import get_current_user
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.schemas.projects import ProjectCreate

router = APIRouter()


@router.get("")
def list_projects(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = ProjectService(ProjectRepository(db))
    return {"data": service.list_projects(current_user), "meta": {}, "errors": []}


@router.post("")
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = ProjectService(ProjectRepository(db))
    return {"data": service.create_project(payload, current_user), "meta": {}, "errors": []}


@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = ProjectService(ProjectRepository(db))
    return {"data": service.get_project(project_id, current_user), "meta": {}, "errors": []}
