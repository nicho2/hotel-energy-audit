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

    def get_latest_by_scenario_ids(
        self,
        scenario_ids: list[UUID],
        project_id: UUID,
    ) -> list[CalculationRun]:
        statement = (
            select(CalculationRun)
            .where(
                CalculationRun.project_id == project_id,
                CalculationRun.scenario_id.in_(scenario_ids),
            )
            .options(
                joinedload(CalculationRun.result_summary),
                joinedload(CalculationRun.economic_result),
                joinedload(CalculationRun.scenario),
            )
            .order_by(CalculationRun.scenario_id.asc(), CalculationRun.created_at.desc())
        )
        runs = self.db.execute(statement).unique().scalars().all()
        latest_by_scenario: dict[UUID, CalculationRun] = {}
        for run in runs:
            if run.scenario_id not in latest_by_scenario:
                latest_by_scenario[run.scenario_id] = run
        return list(latest_by_scenario.values())
