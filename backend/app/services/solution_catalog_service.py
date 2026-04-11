from uuid import UUID

from app.core.exceptions import ForbiddenError, NotFoundError, ValidationError
from app.repositories.solution_catalog_repository import SolutionCatalogRepository
from app.schemas.solutions import (
    SolutionCatalogResponse,
    SolutionDefinitionCreate,
    SolutionDefinitionResponse,
    SolutionDefinitionUpdate,
)


class SolutionCatalogService:
    ADMIN_ROLES = {"org_admin"}

    def __init__(self, repository: SolutionCatalogRepository):
        self.repository = repository

    def list_catalogs(self, current_user) -> list[SolutionCatalogResponse]:
        return [
            SolutionCatalogResponse.model_validate(catalog)
            for catalog in self.repository.list_catalogs(current_user.organization_id)
        ]

    def list_solutions(
        self,
        current_user,
        *,
        country: str | None = None,
        family: str | None = None,
        building_type: str | None = None,
        zone_type: str | None = None,
        scope: str | None = None,
        include_inactive: bool = False,
    ) -> list[SolutionDefinitionResponse]:
        solutions = self.repository.list_solutions(
            current_user.organization_id,
            include_inactive=include_inactive,
        )
        filtered = [
            item
            for item in solutions
            if _matches_filter(country, item.applicable_countries)
            and _matches_filter(building_type, item.applicable_building_types)
            and _matches_filter(zone_type, item.applicable_zone_types)
            and (family is None or item.family == family)
            and (scope is None or item.catalog.scope == scope)
        ]
        return [self._to_solution_response(item) for item in filtered]

    def get_solution_by_code(
        self,
        code: str,
        current_user,
        *,
        include_inactive: bool = False,
    ) -> SolutionDefinitionResponse | None:
        solution = self.repository.get_solution_by_code(
            code,
            current_user.organization_id,
            include_inactive=include_inactive,
        )
        return self._to_solution_response(solution) if solution is not None else None

    def create_solution(self, payload: SolutionDefinitionCreate, current_user) -> SolutionDefinitionResponse:
        self.ensure_admin(current_user)
        catalog = self.repository.get_catalog(payload.catalog_id, current_user.organization_id)
        if catalog is None:
            raise NotFoundError("Solution catalog not found")
        if catalog.scope == "organization_specific" and catalog.organization_id != current_user.organization_id:
            raise ForbiddenError("Cannot create a solution in another organization's catalog")
        existing = self.repository.get_solution_by_code(
            payload.code,
            current_user.organization_id,
            include_inactive=True,
        )
        if existing is not None:
            raise ValidationError(
                "Validation failed",
                field="code",
                details={"reason": "solution code already exists"},
            )
        data = payload.model_dump()
        solution = self.repository.create_solution(**data)
        return self._to_solution_response(solution)

    def update_solution(
        self,
        solution_id: UUID,
        payload: SolutionDefinitionUpdate,
        current_user,
    ) -> SolutionDefinitionResponse:
        self.ensure_admin(current_user)
        solution = self._get_solution_or_404(solution_id, current_user)
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return self._to_solution_response(solution)
        if "catalog_id" in updates:
            catalog = self.repository.get_catalog(updates["catalog_id"], current_user.organization_id)
            if catalog is None:
                raise NotFoundError("Solution catalog not found")
        merged_offer = updates.get("is_commercial_offer", solution.is_commercial_offer)
        merged_reference = updates.get("offer_reference", solution.offer_reference)
        if merged_offer and not merged_reference:
            raise ValidationError(
                "Validation failed",
                field="offer_reference",
                details={"reason": "offer_reference is required for commercial offers"},
            )
        return self._to_solution_response(self.repository.update_solution(solution, **updates))

    def deactivate_solution(self, solution_id: UUID, current_user) -> SolutionDefinitionResponse:
        self.ensure_admin(current_user)
        solution = self._get_solution_or_404(solution_id, current_user)
        return self._to_solution_response(self.repository.update_solution(solution, is_active=False))

    def ensure_admin(self, current_user) -> None:
        if current_user.role not in self.ADMIN_ROLES:
            raise ForbiddenError("Admin permissions required")

    def _get_solution_or_404(self, solution_id: UUID, current_user):
        solution = self.repository.get_solution_by_id(solution_id, current_user.organization_id)
        if solution is None:
            raise NotFoundError("Solution not found")
        return solution

    @staticmethod
    def _to_solution_response(solution) -> SolutionDefinitionResponse:
        return SolutionDefinitionResponse(
            id=solution.id,
            catalog_id=solution.catalog_id,
            catalog_name=solution.catalog.name,
            catalog_version=solution.catalog.version,
            scope=solution.catalog.scope,
            country_code=solution.catalog.country_code,
            organization_id=solution.catalog.organization_id,
            code=solution.code,
            name=solution.name,
            description=solution.description,
            family=solution.family,
            target_scopes=solution.target_scopes,
            applicable_countries=solution.applicable_countries,
            applicable_building_types=solution.applicable_building_types,
            applicable_zone_types=solution.applicable_zone_types,
            bacs_impact_json=solution.bacs_impact_json,
            lifetime_years=solution.lifetime_years,
            default_quantity=solution.default_quantity,
            default_unit=solution.default_unit,
            default_unit_cost=solution.default_unit_cost,
            default_capex=solution.default_capex,
            priority=solution.priority,
            is_commercial_offer=solution.is_commercial_offer,
            offer_reference=solution.offer_reference,
            is_active=solution.is_active,
            created_at=solution.created_at,
            updated_at=solution.updated_at,
        )


def _matches_filter(value: str | None, applicable_values: list[str]) -> bool:
    if value is None:
        return True
    return not applicable_values or value in applicable_values
