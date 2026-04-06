from app.db.base import Base
from app.db.models import Building, Organization, Project, User  # noqa: F401


def test_base_metadata_registers_core_tables() -> None:
    assert set(Base.metadata.tables) >= {"organizations", "users", "projects", "buildings"}
