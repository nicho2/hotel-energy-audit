from typing import Any

from app.repositories.bacs_repository import BacsRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.wizard_step_payload_repository import WizardStepPayloadRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.readiness import CalculationReadinessResponse, ReadinessIssue
from app.services.project_service import ProjectService


STEP_NUMBERS = {
    "project": 1,
    "context": 2,
    "building": 3,
    "zones": 4,
    "usage": 5,
    "systems": 6,
    "bacs": 7,
    "solutions": 8,
    "scenarios": 9,
    "review": 10,
}


class ReadinessService:
    def __init__(
        self,
        project_service: ProjectService,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        technical_system_repository: TechnicalSystemRepository,
        wizard_step_payload_repository: WizardStepPayloadRepository,
        bacs_repository: BacsRepository,
        scenario_repository: ScenarioRepository,
    ):
        self.project_service = project_service
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.technical_system_repository = technical_system_repository
        self.wizard_step_payload_repository = wizard_step_payload_repository
        self.bacs_repository = bacs_repository
        self.scenario_repository = scenario_repository

    def get_calculation_readiness(self, project_id, current_user) -> CalculationReadinessResponse:
        project = self.project_service.get_project(project_id, current_user)
        building = self.building_repository.get_by_project_id(project.id)
        zones = self.zone_repository.list_by_project_id(project.id)
        systems = self.technical_system_repository.list_by_project_id(project.id)
        payloads = {
            payload.step_code: dict(payload.payload_json)
            for payload in self.wizard_step_payload_repository.list_by_project_id(project.id)
        }
        assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
        scenarios = self.scenario_repository.list_by_project_id(project.id)

        issues = build_readiness_issues(
            project=project,
            building=building,
            zones=zones,
            systems=systems,
            usage_payload=payloads.get("usage", {}),
            assessment=assessment,
            scenarios=scenarios,
        )
        blocking_issues = [issue for issue in issues if issue.severity == "error"]
        warnings = [issue for issue in issues if issue.severity == "warning"]

        confidence_level = self._get_confidence_level(
            blocking_issues=blocking_issues,
            warnings=warnings,
            systems=systems,
            assessment=assessment,
        )

        return CalculationReadinessResponse(
            project_id=project.id,
            is_ready=not blocking_issues,
            blocking_issues=blocking_issues,
            warnings=warnings,
            confidence_level=confidence_level,
        )

    @staticmethod
    def _get_confidence_level(
        *,
        blocking_issues: list[ReadinessIssue],
        warnings: list[ReadinessIssue],
        systems: list,
        assessment,
    ) -> str:
        if blocking_issues:
            return "low"

        defined_system_types = {system.system_type for system in systems}
        if not defined_system_types:
            return "low"

        has_major_systems = {"heating", "dhw"} <= defined_system_types
        has_bacs = assessment is not None and bool(getattr(assessment, "selected_functions", []))

        if has_major_systems and has_bacs and not warnings:
            return "high"

        if has_major_systems or len(warnings) <= 2:
            return "medium"

        return "low"


def build_readiness_issues(
    *,
    project,
    building,
    zones: list,
    systems: list,
    usage_payload: dict[str, Any],
    assessment,
    scenarios: list,
) -> list[ReadinessIssue]:
    issues: list[ReadinessIssue] = []

    if project.country_profile_id is None:
        issues.append(
            _issue(
                "country_profile_missing",
                "Country profile is required before calculation.",
                "error",
                "context",
            )
        )
    if project.climate_zone_id is None:
        issues.append(
            _issue(
                "climate_zone_missing",
                "Climate zone is required before calculation.",
                "error",
                "context",
            )
        )

    if building is None:
        issues.append(_issue("building_missing", "Building data is required before calculation.", "error", "building"))
    else:
        reference_area = building.heated_area_m2 or building.gross_floor_area_m2
        if reference_area is None or reference_area <= 0:
            issues.append(
                _issue(
                    "building_area_missing",
                    "A positive heated or gross floor area is required before calculation.",
                    "error",
                    "building",
                )
            )
        if building.number_of_rooms is None or building.number_of_rooms <= 0:
            issues.append(
                _issue(
                    "building_rooms_missing",
                    "A positive room count is required before calculation.",
                    "error",
                    "building",
                )
            )

    if not zones:
        issues.append(_issue("zones_missing", "At least one zone is required before calculation.", "error", "zones"))
    else:
        if any(zone.area_m2 <= 0 for zone in zones):
            issues.append(
                _issue(
                    "zone_area_invalid",
                    "All zones must have a positive area before calculation.",
                    "error",
                    "zones",
                )
            )
        if building is not None:
            reference_area = building.heated_area_m2 or building.gross_floor_area_m2
            if reference_area is not None and sum(zone.area_m2 for zone in zones) > reference_area:
                issues.append(
                    _issue(
                        "zone_area_exceeds_building",
                        "Total zone area must not exceed the building reference area.",
                        "error",
                        "zones",
                    )
                )

    occupancy = _to_float(usage_payload.get("average_occupancy_rate"))
    if occupancy is None:
        issues.append(_issue("usage_occupancy_missing", "Average occupancy is required before calculation.", "error", "usage"))
    elif not 0 <= occupancy <= 1:
        issues.append(_issue("usage_occupancy_invalid", "Average occupancy must be between 0 and 1 internally.", "error", "usage"))
    if not usage_payload.get("ecs_intensity_level"):
        issues.append(_issue("usage_dhw_intensity_missing", "DHW intensity is required before calculation.", "error", "usage"))

    system_types = {system.system_type for system in systems}
    if not systems:
        issues.append(
            _issue(
                "systems_missing",
                "No technical systems are defined; calculation will rely on broad default assumptions.",
                "warning",
                "systems",
            )
        )
    else:
        if "heating" not in system_types:
            issues.append(
                _issue(
                    "heating_system_missing",
                    "No heating system is defined; heating estimates will rely on weaker assumptions.",
                    "warning",
                    "systems",
                )
            )
        if "dhw" not in system_types:
            issues.append(
                _issue(
                    "dhw_system_missing",
                    "No DHW system is defined; domestic hot water assumptions remain approximate.",
                    "warning",
                    "systems",
                )
            )

    selected_functions = getattr(assessment, "selected_functions", []) if assessment is not None else []
    if assessment is None or not selected_functions:
        issues.append(
            _issue(
                "bacs_assessment_missing",
                "BACS assessment is missing; BACS impact will use conservative defaults.",
                "warning",
                "bacs",
            )
        )

    if not scenarios:
        issues.append(_issue("scenario_missing", "At least one scenario must be created before calculation.", "error", "scenarios"))

    return issues


def _issue(code: str, message: str, severity: str, step_code: str) -> ReadinessIssue:
    return ReadinessIssue(
        code=code,
        message=message,
        severity=severity,
        step_code=step_code,
        step=STEP_NUMBERS[step_code],
    )


def _to_float(value: Any) -> float | None:
    if value in {None, ""}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
