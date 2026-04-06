from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.building import Building


class BuildingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_project_id(self, project_id: UUID) -> Building | None:
        statement = select(Building).where(Building.project_id == project_id)
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> Building:
        building = Building(**kwargs)
        self.db.add(building)
        self.db.commit()
        self.db.refresh(building)
        return building

    def update(self, building: Building, **kwargs: object) -> Building:
        for field, value in kwargs.items():
            setattr(building, field, value)

        self.db.add(building)
        self.db.commit()
        self.db.refresh(building)
        return building
