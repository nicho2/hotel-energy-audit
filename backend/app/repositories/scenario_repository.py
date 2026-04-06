from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.scenario import Scenario


class ScenarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, scenario_id: UUID, project_id: UUID) -> Scenario | None:
        statement = select(Scenario).where(
            Scenario.id == scenario_id,
            Scenario.project_id == project_id,
        )
        return self.db.scalar(statement)
