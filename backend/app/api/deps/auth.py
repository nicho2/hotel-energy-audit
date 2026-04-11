from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.api.deps.db import get_db
from app.core.config import settings
from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.models.project import Project
from app.db.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/login",
    auto_error=False,
)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if token is None:
        raise UnauthorizedError("Authentication required")

    payload = decode_access_token(token)
    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    subject = payload.get("sub")
    if not subject:
        raise UnauthorizedError("Invalid token payload")
    try:
        user_id = UUID(subject)
    except ValueError as exc:
        raise UnauthorizedError("Invalid token subject") from exc

    user = UserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("User not found or inactive")
    if payload.get("organization_id") != str(user.organization_id):
        raise UnauthorizedError("Invalid token organization")
    if payload.get("role") != user.role:
        raise UnauthorizedError("Invalid token role")
    return user


def require_role(*allowed_roles: str):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenError("Insufficient role")
        return current_user

    return dependency


def require_org_admin(current_user: User = Depends(require_role("org_admin"))) -> User:
    return current_user


def require_project_access(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Project:
    project = ProjectRepository(db).get_by_id(project_id, current_user.organization_id)
    if project is None:
        raise NotFoundError("Project not found")
    return project
