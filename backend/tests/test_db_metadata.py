from app.db.base import Base
from app.db.models import (  # noqa: F401
    BacsAssessment,
    BacsFunctionDefinition,
    BacsSelectedFunction,
    BrandingProfile,
    CalculationRun,
    Building,
    BuildingZone,
    EconomicResult,
    GeneratedReport,
    Organization,
    Project,
    ResultByUse,
    ResultByZone,
    ResultSummary,
    Scenario,
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
        "branding_profiles",
        "scenarios",
        "calculation_runs",
        "result_summaries",
        "economic_results",
        "generated_reports",
        "result_by_use",
        "result_by_zone",
    }
