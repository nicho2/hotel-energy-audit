from app.core.exceptions import NotFoundError
from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.assumptions import (
    AssumptionItemResponse,
    AssumptionSectionResponse,
    ProjectAssumptionsResponse,
)


class AssumptionsService:
    FALLBACK_ENGINE_VERSION = "placeholder-v1"

    def __init__(
        self,
        project_repository: ProjectRepository,
        building_repository: BuildingRepository,
        bacs_repository: BacsRepository,
        calculation_repository: CalculationRepository,
    ):
        self.project_repository = project_repository
        self.building_repository = building_repository
        self.bacs_repository = bacs_repository
        self.calculation_repository = calculation_repository

    def get_project_assumptions(self, project_id, current_user) -> ProjectAssumptionsResponse:
        project = self.project_repository.get_by_id(project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")

        building = self.building_repository.get_by_project_id(project.id)
        bacs_assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
        latest_run = self.calculation_repository.get_latest_by_project(project.id)
        economic = latest_run.economic_result if latest_run is not None else None

        sections = [
            self._context_section(project, latest_run),
            self._climate_section(),
            self._building_section(building),
            self._economic_section(economic),
            self._bacs_section(bacs_assessment),
            self._engine_section(latest_run),
        ]

        return ProjectAssumptionsResponse(
            project_id=project.id,
            calculation_run_id=latest_run.id if latest_run is not None else None,
            scenario_name=latest_run.scenario.name if latest_run is not None and latest_run.scenario is not None else None,
            engine_version=latest_run.engine_version if latest_run is not None else self.FALLBACK_ENGINE_VERSION,
            generated_at=latest_run.created_at if latest_run is not None else None,
            warnings=latest_run.warnings_json if latest_run is not None else ["No calculation run is available yet."],
            sections=sections,
        )

    def _context_section(self, project, latest_run) -> AssumptionSectionResponse:
        return AssumptionSectionResponse(
            key="context",
            title="Context",
            items=[
                self._item("project", "Project", project.name, "configured"),
                self._item("client", "Client", project.client_name, "configured", default_value="Not provided"),
                self._item("building_type", "Building type", project.building_type, "configured"),
                self._item("project_goal", "Project goal", project.project_goal, "configured", default_value="Pre-audit / scenario comparison"),
                self._item(
                    "scenario_used",
                    "Scenario used",
                    latest_run.scenario.name if latest_run is not None and latest_run.scenario is not None else None,
                    "calculated" if latest_run is not None else "defaulted",
                    default_value="No calculated scenario yet",
                    warning=latest_run is None,
                ),
            ],
        )

    def _climate_section(self) -> AssumptionSectionResponse:
        return AssumptionSectionResponse(
            key="climate",
            title="Climate",
            items=[
                self._item(
                    "climate_profile",
                    "Climate profile",
                    None,
                    "defaulted",
                    default_value="Standard MVP climate profile",
                    note="Country and climate reference data are planned for a later admin configuration slice.",
                    warning=True,
                ),
                self._item(
                    "weather_normalization",
                    "Weather normalization",
                    None,
                    "defaulted",
                    default_value="Annual simplified correction",
                ),
            ],
        )

    def _building_section(self, building) -> AssumptionSectionResponse:
        return AssumptionSectionResponse(
            key="building",
            title="Building defaults",
            items=[
                self._item("building_name", "Building name", getattr(building, "name", None), "configured", default_value="Not provided"),
                self._item("construction_period", "Construction period", getattr(building, "construction_period", None), "configured", default_value="Generic existing building"),
                self._item("gross_floor_area", "Gross floor area", self._area(getattr(building, "gross_floor_area_m2", None)), "configured", default_value="Not provided", warning=building is None or getattr(building, "gross_floor_area_m2", None) is None),
                self._item("heated_area", "Heated area", self._area(getattr(building, "heated_area_m2", None)), "configured", default_value="Falls back to gross area when needed"),
                self._item("rooms", "Rooms", getattr(building, "number_of_rooms", None), "configured", default_value="Not provided"),
                self._item("main_orientation", "Main orientation", getattr(building, "main_orientation", None), "configured", default_value="mixed"),
                self._item("compactness", "Compactness", getattr(building, "compactness_level", None), "configured", default_value="standard"),
            ],
        )

    def _economic_section(self, economic) -> AssumptionSectionResponse:
        return AssumptionSectionResponse(
            key="economic",
            title="Economic defaults",
            items=[
                self._item("capex", "CAPEX", self._currency(getattr(economic, "total_capex", None)), "calculated", default_value="Pending calculation", warning=economic is None),
                self._item("annual_savings", "Annual savings", self._currency(getattr(economic, "annual_cost_savings", None)), "calculated", default_value="Pending calculation", warning=economic is None),
                self._item("simple_payback", "Simple payback", self._years(getattr(economic, "simple_payback_years", None)), "calculated", default_value="Pending calculation", warning=economic is None),
                self._item("npv", "NPV", self._currency(getattr(economic, "npv", None)), "calculated", default_value="Pending calculation", warning=economic is None),
                self._item("irr", "IRR", self._percent(getattr(economic, "irr", None)), "calculated", default_value="Pending calculation", warning=economic is None),
            ],
        )

    def _bacs_section(self, assessment) -> AssumptionSectionResponse:
        selected_count = len(assessment.selected_functions) if assessment is not None else None
        return AssumptionSectionResponse(
            key="bacs",
            title="BACS rules",
            items=[
                self._item("bacs_version", "BACS version", getattr(assessment, "version", None), "configured", default_value="v1"),
                self._item("selected_functions", "Selected functions", selected_count, "configured", default_value="0", warning=not selected_count),
                self._item("manual_override", "Manual override", getattr(assessment, "manual_override_class", None), "configured", default_value="None"),
                self._item("scoring_rule", "Scoring rule", None, "defaulted", default_value="Weighted selected BACS functions by domain"),
            ],
        )

    def _engine_section(self, latest_run) -> AssumptionSectionResponse:
        return AssumptionSectionResponse(
            key="engine",
            title="Engine version",
            items=[
                self._item("engine_version", "Engine version", getattr(latest_run, "engine_version", None), "calculated", default_value=self.FALLBACK_ENGINE_VERSION),
                self._item("calculation_status", "Calculation status", getattr(latest_run, "status", None), "calculated", default_value="No run yet", warning=latest_run is None),
                self._item("snapshot_policy", "Snapshot policy", None, "defaulted", default_value="Calculation input snapshot stored with each run"),
                self._item("engine_scope", "Engine scope", None, "defaulted", default_value="Simplified annual estimation, not regulatory simulation"),
            ],
        )

    @staticmethod
    def _item(key, label, value, source, *, default_value=None, note=None, warning=False) -> AssumptionItemResponse:
        has_value = value is not None and value != ""
        return AssumptionItemResponse(
            key=key,
            label=label,
            value=str(value if has_value else default_value),
            source=source if has_value or source == "calculated" else "defaulted",
            note=note,
            warning=warning,
        )

    @staticmethod
    def _area(value) -> str | None:
        return f"{value:.0f} m2" if value is not None else None

    @staticmethod
    def _currency(value) -> str | None:
        return f"{value:.0f} EUR" if value is not None else None

    @staticmethod
    def _years(value) -> str | None:
        return f"{value:.1f} years" if value is not None else None

    @staticmethod
    def _percent(value) -> str | None:
        return f"{value * 100:.1f}%" if value is not None else None
