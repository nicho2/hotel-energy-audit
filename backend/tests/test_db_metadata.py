from app.db.base import Base
from app.db.models import (  # noqa: F401
    BacsAssessment,
    BacsFunctionDefinition,
    BacsSelectedFunction,
    Building,
    BuildingZone,
    Organization,
    Project,
    TechnicalSystem,
    User,
)


def test_base_metadata_registers_core_tables() -> None:
    assert set(Base.metadata.tables) >= {
        "organizations",
        "users",
        "projects",
        "buildings",
        "building_zones",
        "technical_systems",
        "bacs_assessments",
        "bacs_function_definitions",
        "bacs_selected_functions",
    }
