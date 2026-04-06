from app.repositories.building_repository import BuildingRepository
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.readiness import CalculationReadinessResponse, ReadinessIssue
from app.services.project_service import ProjectService


class ReadinessService:
    def __init__(
        self,
        project_service: ProjectService,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        technical_system_repository: TechnicalSystemRepository,
    ):
        self.project_service = project_service
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.technical_system_repository = technical_system_repository

    def get_calculation_readiness(self, project_id, current_user) -> CalculationReadinessResponse:
        project = self.project_service.get_project(project_id, current_user)
        building = self.building_repository.get_by_project_id(project.id)
        zones = self.zone_repository.list_by_project_id(project.id)
        systems = self.technical_system_repository.list_by_project_id(project.id)

        blocking_issues: list[ReadinessIssue] = []
        warnings: list[ReadinessIssue] = []

        if building is None:
            blocking_issues.append(
                ReadinessIssue(
                    code="building_missing",
                    message="Building data is required before calculation.",
                )
            )

        if not zones:
            blocking_issues.append(
                ReadinessIssue(
                    code="zones_missing",
                    message="At least one zone is required before calculation.",
                )
            )

        has_heating = any(system.system_type == "heating" for system in systems)
        has_dhw = any(system.system_type == "dhw" for system in systems)

        if not has_heating:
            warnings.append(
                ReadinessIssue(
                    code="heating_system_missing",
                    message="No heating system is defined; calculation will rely on weaker assumptions.",
                )
            )

        if not has_dhw:
            warnings.append(
                ReadinessIssue(
                    code="dhw_system_missing",
                    message="No DHW system is defined; domestic hot water assumptions remain approximate.",
                )
            )

        warnings.append(
            ReadinessIssue(
                code="reference_scenario_implicit",
                message="Scenarios are not modeled yet; the current project data is used as the implicit reference scenario.",
            )
        )

        confidence_level = self._get_confidence_level(
            has_building=building is not None,
            zone_count=len(zones),
            systems=systems,
        )

        return CalculationReadinessResponse(
            project_id=project.id,
            is_ready=not blocking_issues,
            blocking_issues=blocking_issues,
            warnings=warnings,
            confidence_level=confidence_level,
        )

    @staticmethod
    def _get_confidence_level(*, has_building: bool, zone_count: int, systems: list) -> str:
        defined_system_types = {system.system_type for system in systems}

        if has_building and zone_count >= 1 and {"heating", "dhw"} <= defined_system_types:
            return "high"

        if has_building and zone_count >= 1 and defined_system_types:
            return "medium"

        return "low"
