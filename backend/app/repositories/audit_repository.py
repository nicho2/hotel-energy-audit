from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.audit_log import AuditLog


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs: object) -> AuditLog:
        item = AuditLog(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_for_project(self, project_id: UUID, organization_id: UUID) -> list[AuditLog]:
        statement = (
            select(AuditLog)
            .where(
                AuditLog.organization_id == organization_id,
                AuditLog.project_id == project_id,
            )
            .order_by(AuditLog.timestamp.desc())
        )
        return list(self.db.scalars(statement).all())

    def list_for_scenario(
        self,
        *,
        project_id: UUID,
        scenario_id: UUID,
        organization_id: UUID,
    ) -> list[AuditLog]:
        statement = (
            select(AuditLog)
            .where(
                AuditLog.organization_id == organization_id,
                AuditLog.project_id == project_id,
                AuditLog.scenario_id == scenario_id,
            )
            .order_by(AuditLog.timestamp.desc())
        )
        return list(self.db.scalars(statement).all())

    def list_filtered(
        self,
        organization_id: UUID,
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
    ) -> list[AuditLog]:
        statement = select(AuditLog).where(AuditLog.organization_id == organization_id)
        if entity_type is not None:
            statement = statement.where(AuditLog.entity_type == entity_type)
        if entity_id is not None:
            statement = statement.where(AuditLog.entity_id == entity_id)
        if action is not None:
            statement = statement.where(AuditLog.action == action)
        if project_id is not None:
            statement = statement.where(AuditLog.project_id == project_id)
        if scenario_id is not None:
            statement = statement.where(AuditLog.scenario_id == scenario_id)
        if user_id is not None:
            statement = statement.where(AuditLog.user_id == user_id)
        if date_from is not None:
            statement = statement.where(AuditLog.timestamp >= date_from)
        if date_to is not None:
            statement = statement.where(AuditLog.timestamp <= date_to)
        statement = statement.order_by(AuditLog.timestamp.desc()).limit(limit)
        return list(self.db.scalars(statement).all())
