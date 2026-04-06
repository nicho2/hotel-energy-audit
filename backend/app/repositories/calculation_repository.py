from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.calculation_run import CalculationRun
from app.db.models.economic_result import EconomicResult
from app.db.models.result_by_use import ResultByUse
from app.db.models.result_by_zone import ResultByZone
from app.db.models.result_summary import ResultSummary


class CalculationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_run(
        self,
        *,
        project_id: UUID,
        scenario_id: UUID,
        status: str,
        engine_version: str,
        input_snapshot: dict,
        messages_json: list[str],
        warnings_json: list[str],
    ) -> CalculationRun:
        run = CalculationRun(
            project_id=project_id,
            scenario_id=scenario_id,
            status=status,
            engine_version=engine_version,
            input_snapshot=input_snapshot,
            messages_json=messages_json,
            warnings_json=warnings_json,
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def create_result_summary(self, calculation_run_id: UUID, **kwargs: object) -> ResultSummary:
        summary = ResultSummary(calculation_run_id=calculation_run_id, **kwargs)
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        return summary

    def create_economic_result(self, calculation_run_id: UUID, **kwargs: object) -> EconomicResult:
        economic = EconomicResult(calculation_run_id=calculation_run_id, **kwargs)
        self.db.add(economic)
        self.db.commit()
        self.db.refresh(economic)
        return economic

    def create_results_by_use(self, calculation_run_id: UUID, items: list[dict]) -> list[ResultByUse]:
        results = [ResultByUse(calculation_run_id=calculation_run_id, **item) for item in items]
        self.db.add_all(results)
        self.db.commit()
        for result in results:
            self.db.refresh(result)
        return results

    def create_results_by_zone(self, calculation_run_id: UUID, items: list[dict]) -> list[ResultByZone]:
        results = [ResultByZone(calculation_run_id=calculation_run_id, **item) for item in items]
        self.db.add_all(results)
        self.db.commit()
        for result in results:
            self.db.refresh(result)
        return results

    def get_latest_by_scenario(self, scenario_id: UUID, project_id: UUID) -> CalculationRun | None:
        statement = (
            select(CalculationRun)
            .where(
                CalculationRun.scenario_id == scenario_id,
                CalculationRun.project_id == project_id,
            )
            .options(
                joinedload(CalculationRun.result_summary),
                joinedload(CalculationRun.economic_result),
            )
            .order_by(CalculationRun.created_at.desc())
        )
        return self.db.scalars(statement).first()
