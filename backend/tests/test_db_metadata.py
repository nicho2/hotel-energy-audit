from app.db.base import Base
from app.db.models import Building, BuildingZone, Organization, Project, TechnicalSystem, User  # noqa: F401


def test_base_metadata_registers_core_tables() -> None:
    assert set(Base.metadata.tables) >= {
        "organizations",
        "users",
        "projects",
        "buildings",
        "building_zones",
        "technical_systems",
    }
