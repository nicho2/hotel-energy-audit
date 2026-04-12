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
    ClimateZone,
    CountryProfile,
    EconomicResult,
    GeneratedReport,
    Organization,
    Project,
    ProjectTemplate,
    ResultByUse,
    ResultByZone,
    ResultSummary,
    Scenario,
    ScenarioSolutionAssignment,
    SolutionCatalog,
    SolutionDefinition,
    TechnicalSystem,
    UsageProfile,
    User,
    WizardStepPayload,
)


def test_base_metadata_registers_core_tables() -> None:
    assert set(Base.metadata.tables) >= {
        "organizations",
        "users",
        "projects",
        "project_templates",
        "country_profiles",
        "climate_zones",
        "usage_profiles",
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
        "wizard_step_payloads",
    }


def test_project_metadata_exposes_country_and_climate_columns() -> None:
    project_columns = Base.metadata.tables["projects"].columns

    assert "country_profile_id" in project_columns
    assert "climate_zone_id" in project_columns


def test_wizard_step_payload_metadata_exposes_project_step_unique_constraint() -> None:
    table = Base.metadata.tables["wizard_step_payloads"]

    assert "project_id" in table.columns
    assert "step_code" in table.columns
    assert "payload_json" in table.columns
    assert any(
        constraint.name == "uq_wizard_step_payloads_project_step"
        for constraint in table.constraints
    )
