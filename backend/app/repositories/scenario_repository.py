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

    def list_by_ids(self, scenario_ids: list[UUID], project_id: UUID) -> list[Scenario]:
        statement = (
            select(Scenario)
            .where(
                Scenario.project_id == project_id,
                Scenario.id.in_(scenario_ids),
            )
            .order_by(Scenario.created_at.asc(), Scenario.name.asc())
        )
        return list(self.db.scalars(statement).all())

    def list_by_project_id(self, project_id: UUID) -> list[Scenario]:
        statement = (
            select(Scenario)
            .where(Scenario.project_id == project_id)
            .order_by(Scenario.created_at.asc(), Scenario.name.asc())
        )
        return list(self.db.scalars(statement).all())

    def create(self, **kwargs: object) -> Scenario:
        scenario = Scenario(**kwargs)
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def update(self, scenario: Scenario, **kwargs: object) -> Scenario:
        for field, value in kwargs.items():
            setattr(scenario, field, value)
        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)
        return scenario

    def delete(self, scenario: Scenario) -> None:
        self.db.delete(scenario)
        self.db.commit()
