from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.generated_report import GeneratedReport


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs: object) -> GeneratedReport:
        report = GeneratedReport(**kwargs)
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_by_id(self, report_id: UUID, organization_id: UUID) -> GeneratedReport | None:
        statement = select(GeneratedReport).where(
            GeneratedReport.id == report_id,
            GeneratedReport.organization_id == organization_id,
        )
        return self.db.scalar(statement)
