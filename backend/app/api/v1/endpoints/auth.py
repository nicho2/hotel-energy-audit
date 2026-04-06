from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import CurrentUserResponse, LoginRequest, LoginResponse
from app.schemas.common import ApiResponse, success_response
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse[LoginResponse]:
    service = AuthService(UserRepository(db))
    return success_response(service.login(payload.email, payload.password))


@router.get("/me", response_model=ApiResponse[CurrentUserResponse])
def me(current_user: User = Depends(get_current_user)) -> ApiResponse[CurrentUserResponse]:
    return success_response(CurrentUserResponse.model_validate(current_user))
