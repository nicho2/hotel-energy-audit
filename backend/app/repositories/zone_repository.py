from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.building_zone import BuildingZone


class ZoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_project_id(self, project_id: UUID) -> list[BuildingZone]:
        statement = (
            select(BuildingZone)
            .where(BuildingZone.project_id == project_id)
            .order_by(BuildingZone.order_index.asc(), BuildingZone.name.asc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, zone_id: UUID, project_id: UUID) -> BuildingZone | None:
        statement = select(BuildingZone).where(
            BuildingZone.id == zone_id,
            BuildingZone.project_id == project_id,
        )
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> BuildingZone:
        zone = BuildingZone(**kwargs)
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update(self, zone: BuildingZone, **kwargs: object) -> BuildingZone:
        for field, value in kwargs.items():
            setattr(zone, field, value)

        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone: BuildingZone) -> None:
        self.db.delete(zone)
        self.db.commit()

    def replace_for_project(self, project_id: UUID, zones_data: list[dict]) -> list[BuildingZone]:
        self.db.execute(delete(BuildingZone).where(BuildingZone.project_id == project_id))
        zones = [BuildingZone(project_id=project_id, **zone_data) for zone_data in zones_data]
        self.db.add_all(zones)
        self.db.commit()
        for zone in zones:
            self.db.refresh(zone)
        return zones
