from datetime import datetime
from uuid import UUID

from app.core.exceptions import ForbiddenError
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit import AuditLogResponse


class AuditService:
    ADMIN_ROLES = {"org_admin"}

    def __init__(self, repository: AuditRepository):
        self.repository = repository

    def log(
        self,
        *,
        entity_type: str,
        entity_id: UUID,
        action: str,
        current_user,
        before_json: dict | None = None,
        after_json: dict | None = None,
        project_id: UUID | None = None,
        scenario_id: UUID | None = None,
    ) -> AuditLogResponse:
        item = self.repository.create(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            before_json=_clean_payload(before_json),
            after_json=_clean_payload(after_json),
            user_id=current_user.id if current_user is not None else None,
            organization_id=current_user.organization_id,
            project_id=project_id,
            scenario_id=scenario_id,
        )
        return AuditLogResponse.model_validate(item)

    def list_audit_logs(
        self,
        current_user,
        *,
        entity_type: str | None = None,
        entity_id: UUID | None = None,
        action: str | None = None,
        project_id: UUID | None = None,
        scenario_id: UUID | None = None,
        user_id: UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 100,
    ) -> list[AuditLogResponse]:
        self.ensure_admin(current_user)
        items = self.repository.list_filtered(
            current_user.organization_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            project_id=project_id,
            scenario_id=scenario_id,
            user_id=user_id,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
        )
        return [AuditLogResponse.model_validate(item) for item in items]

    def ensure_admin(self, current_user) -> None:
        if current_user.role not in self.ADMIN_ROLES:
            raise ForbiddenError("Admin permissions required")


def _clean_payload(payload: dict | None) -> dict | None:
    if payload is None:
        return None
    return {
        key: _json_safe(value)
        for key, value in payload.items()
        if key not in {"password", "password_hash", "secret", "token"}
    }


def _json_safe(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return _clean_payload(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value
