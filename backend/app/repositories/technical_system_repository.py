from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.technical_system import TechnicalSystem


class TechnicalSystemRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_project_id(self, project_id: UUID) -> list[TechnicalSystem]:
        statement = (
            select(TechnicalSystem)
            .where(TechnicalSystem.project_id == project_id)
            .order_by(TechnicalSystem.order_index.asc(), TechnicalSystem.name.asc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, system_id: UUID, project_id: UUID) -> TechnicalSystem | None:
        statement = select(TechnicalSystem).where(
            TechnicalSystem.id == system_id,
            TechnicalSystem.project_id == project_id,
        )
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> TechnicalSystem:
        system = TechnicalSystem(**kwargs)
        self.db.add(system)
        self.db.commit()
        self.db.refresh(system)
        return system

    def update(self, system: TechnicalSystem, **kwargs: object) -> TechnicalSystem:
        for field, value in kwargs.items():
            setattr(system, field, value)

        self.db.add(system)
        self.db.commit()
        self.db.refresh(system)
        return system

    def delete(self, system: TechnicalSystem) -> None:
        self.db.delete(system)
        self.db.commit()
