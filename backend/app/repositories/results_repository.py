from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.calculation_run import CalculationRun


class ResultsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_latest_by_scenario(self, scenario_id: UUID, project_id: UUID) -> CalculationRun | None:
        statement = (
            select(CalculationRun)
            .where(
                CalculationRun.scenario_id == scenario_id,
                CalculationRun.project_id == project_id,
            )
            .options(
                joinedload(CalculationRun.results_by_use),
                joinedload(CalculationRun.results_by_zone),
            )
            .order_by(CalculationRun.created_at.desc())
        )
        return self.db.execute(statement).unique().scalars().first()
