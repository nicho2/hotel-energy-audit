from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.scenario_solution_assignment import ScenarioSolutionAssignment


class ScenarioSolutionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_scenario_id(self, scenario_id: UUID) -> list[ScenarioSolutionAssignment]:
        statement = (
            select(ScenarioSolutionAssignment)
            .where(ScenarioSolutionAssignment.scenario_id == scenario_id)
            .order_by(ScenarioSolutionAssignment.created_at.asc(), ScenarioSolutionAssignment.solution_code.asc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, assignment_id: UUID, scenario_id: UUID) -> ScenarioSolutionAssignment | None:
        statement = select(ScenarioSolutionAssignment).where(
            ScenarioSolutionAssignment.id == assignment_id,
            ScenarioSolutionAssignment.scenario_id == scenario_id,
        )
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> ScenarioSolutionAssignment:
        assignment = ScenarioSolutionAssignment(**kwargs)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def update(self, assignment: ScenarioSolutionAssignment, **kwargs: object) -> ScenarioSolutionAssignment:
        for field, value in kwargs.items():
            setattr(assignment, field, value)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def delete(self, assignment: ScenarioSolutionAssignment) -> None:
        self.db.delete(assignment)
        self.db.commit()
