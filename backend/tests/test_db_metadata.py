from app.db.base import Base
from app.db.models import (  # noqa: F401
    BacsAssessment,
    BacsFunctionDefinition,
    BacsSelectedFunction,
    AuditLog,
    BrandingProfile,
    CalculationAssumptionSet,
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
    ScenarioSolutionAssignment,
    SolutionCatalog,
    SolutionDefinition,
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
        "audit_logs",
        "branding_profiles",
        "calculation_assumption_sets",
        "scenarios",
        "scenario_solution_assignments",
        "solution_catalogs",
        "solution_definitions",
        "calculation_runs",
        "result_summaries",
        "economic_results",
        "generated_reports",
        "result_by_use",
        "result_by_zone",
    }


def test_project_metadata_exposes_country_and_climate_columns() -> None:
    project_columns = Base.metadata.tables["projects"].columns

    assert "country_profile_id" in project_columns
    assert "climate_zone_id" in project_columns
