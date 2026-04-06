from app.db.base import Base


def test_base_metadata_registers_core_tables() -> None:
    assert set(Base.metadata.tables) >= {"organizations", "users", "projects"}
