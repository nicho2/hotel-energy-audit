from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.scenario_solution_repository import ScenarioSolutionRepository
from app.services.solution_catalog_service import SolutionCatalogService
from app.services.project_service import ProjectService


class ScenarioService:
    def __init__(
        self,
        scenario_repository: ScenarioRepository,
        scenario_solution_repository: ScenarioSolutionRepository,
        project_service: ProjectService,
        solution_catalog_service: SolutionCatalogService,
    ):
        self.scenario_repository = scenario_repository
        self.scenario_solution_repository = scenario_solution_repository
        self.project_service = project_service
        self.solution_catalog_service = solution_catalog_service

    def list_scenarios(self, project_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        return self.scenario_repository.list_by_project_id(project.id)

    def create_scenario(self, project_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        data = payload.model_dump()
        if data.get("is_reference"):
            self._clear_reference_flag(project.id)
        return self.scenario_repository.create(
            project_id=project.id,
            name=data["name"],
            description=data.get("description"),
            scenario_type=data.get("scenario_type", "custom"),
            status="draft",
            derived_from_scenario_id=data.get("derived_from_scenario_id"),
            is_reference=data.get("is_reference", False),
        )

    def update_scenario(self, project_id, scenario_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return scenario
        if updates.get("is_reference"):
            self._clear_reference_flag(project.id, keep_id=scenario.id)
        return self.scenario_repository.update(scenario, **updates)

    def duplicate_scenario(self, project_id, scenario_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")

        duplicated = self.scenario_repository.create(
            project_id=project.id,
            name=payload.name or f"{scenario.name} copy",
            description=scenario.description,
            scenario_type=scenario.scenario_type,
            status="draft",
            derived_from_scenario_id=scenario.id,
            is_reference=False,
        )

        for assignment in self.scenario_solution_repository.list_by_scenario_id(scenario.id):
            self.scenario_solution_repository.create(
                scenario_id=duplicated.id,
                solution_code=assignment.solution_code,
                target_scope=assignment.target_scope,
                target_zone_id=assignment.target_zone_id,
                target_system_id=assignment.target_system_id,
                quantity=assignment.quantity,
                unit_cost_override=assignment.unit_cost_override,
                capex_override=assignment.capex_override,
                maintenance_override=assignment.maintenance_override,
                gain_override_percent=assignment.gain_override_percent,
                notes=assignment.notes,
                is_selected=assignment.is_selected,
            )

        return duplicated

    def list_catalog(
        self,
        current_user,
        *,
        country: str | None = None,
        family: str | None = None,
        building_type: str | None = None,
        zone_type: str | None = None,
        scope: str | None = None,
        include_inactive: bool = False,
    ):
        return self.solution_catalog_service.list_solutions(
            current_user,
            country=country,
            family=family,
            building_type=building_type,
            zone_type=zone_type,
            scope=scope,
            include_inactive=include_inactive,
        )

    def list_assignments(self, project_id, scenario_id, current_user):
        scenario = self._get_project_scenario(project_id, scenario_id, current_user)
        return self.scenario_solution_repository.list_by_scenario_id(scenario.id)

    def create_assignment(self, project_id, scenario_id, payload, current_user):
        scenario = self._get_project_scenario(project_id, scenario_id, current_user)
        self._validate_solution_code(payload.solution_code, current_user)
        data = payload.model_dump()
        self._validate_target_scope(data)
        return self.scenario_solution_repository.create(scenario_id=scenario.id, **data)

    def update_assignment(self, project_id, scenario_id, assignment_id, payload, current_user):
        scenario = self._get_project_scenario(project_id, scenario_id, current_user)
        assignment = self.scenario_solution_repository.get_by_id(assignment_id, scenario.id)
        if assignment is None:
            raise NotFoundError("Scenario solution assignment not found")
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return assignment
        merged = {
            "target_scope": assignment.target_scope,
            "target_zone_id": assignment.target_zone_id,
            "target_system_id": assignment.target_system_id,
            **updates,
        }
        self._validate_target_scope(merged)
        return self.scenario_solution_repository.update(assignment, **updates)

    def delete_assignment(self, project_id, scenario_id, assignment_id, current_user):
        scenario = self._get_project_scenario(project_id, scenario_id, current_user)
        assignment = self.scenario_solution_repository.get_by_id(assignment_id, scenario.id)
        if assignment is None:
            raise NotFoundError("Scenario solution assignment not found")
        self.scenario_solution_repository.delete(assignment)
        return assignment

    def _get_project_scenario(self, project_id, scenario_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        scenario = self.scenario_repository.get_by_id(scenario_id, project.id)
        if scenario is None:
            raise NotFoundError("Scenario not found")
        return scenario

    def _clear_reference_flag(self, project_id, keep_id=None) -> None:
        for item in self.scenario_repository.list_by_project_id(project_id):
            if keep_id is not None and item.id == keep_id:
                continue
            if item.is_reference:
                self.scenario_repository.update(item, is_reference=False)

    @staticmethod
    def _validate_target_scope(data: dict) -> None:
        if data["target_scope"] == "zone" and data.get("target_zone_id") is None:
            raise ValidationError(
                "Validation failed",
                field="target_zone_id",
                details={"reason": "target_zone_id is required when target_scope is zone"},
            )
        if data["target_scope"] == "system" and data.get("target_system_id") is None:
            raise ValidationError(
                "Validation failed",
                field="target_system_id",
                details={"reason": "target_system_id is required when target_scope is system"},
            )

    def _validate_solution_code(self, solution_code: str, current_user) -> None:
        if self.solution_catalog_service.get_solution_by_code(solution_code, current_user) is None:
            raise ValidationError(
                "Validation failed",
                field="solution_code",
                details={"reason": "solution_code must exist in the active catalog"},
            )
