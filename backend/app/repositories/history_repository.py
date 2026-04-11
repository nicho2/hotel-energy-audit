from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.repositories.scenario_repository import ScenarioRepository


class HistoryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.scenario_repository = ScenarioRepository(db)
        self.report_repository = ReportRepository(db)

    def list_scenarios(self, project_id: UUID):
        return self.scenario_repository.list_by_project_id(project_id)

    def list_reports(self, project_id: UUID, organization_id: UUID):
        return self.report_repository.list_by_project_id(project_id, organization_id)
