from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.audit_repository import AuditRepository
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.scenario_repository import ScenarioRepository
from app.repositories.scenario_solution_repository import ScenarioSolutionRepository
from app.repositories.solution_catalog_repository import SolutionCatalogRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.scenarios import (
    ScenarioCreate,
    ScenarioDuplicateRequest,
    ScenarioResponse,
    ScenarioSolutionAssignmentCreate,
    ScenarioSolutionAssignmentResponse,
    ScenarioSolutionAssignmentUpdate,
    ScenarioSolutionDetailedResponse,
    ScenarioUpdate,
    SolutionCatalogItemResponse,
)
from app.services.audit_service import AuditService
from app.services.project_service import ProjectService
from app.services.scenario_service import ScenarioService
from app.services.solution_catalog_service import SolutionCatalogService

router = APIRouter()


def get_scenario_service(db: Session) -> ScenarioService:
    project_service = ProjectService(ProjectRepository(db), BrandingRepository(db))
    audit_service = AuditService(AuditRepository(db))
    return ScenarioService(
        scenario_repository=ScenarioRepository(db),
        scenario_solution_repository=ScenarioSolutionRepository(db),
        project_service=project_service,
        solution_catalog_service=SolutionCatalogService(SolutionCatalogRepository(db)),
        audit_service=audit_service,
    )


@router.get("/{project_id}/scenarios", response_model=ApiResponse[list[ScenarioResponse]])
def list_scenarios(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ScenarioResponse]]:
    service = get_scenario_service(db)
    scenarios = service.list_scenarios(project_id, current_user)
    return success_response([ScenarioResponse.model_validate(item) for item in scenarios])


@router.post("/{project_id}/scenarios", response_model=ApiResponse[ScenarioResponse])
def create_scenario(
    project_id: UUID,
    payload: ScenarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioResponse]:
    service = get_scenario_service(db)
    scenario = service.create_scenario(project_id, payload, current_user)
    return success_response(ScenarioResponse.model_validate(scenario))


@router.patch("/{project_id}/scenarios/{scenario_id}", response_model=ApiResponse[ScenarioResponse])
def update_scenario(
    project_id: UUID,
    scenario_id: UUID,
    payload: ScenarioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioResponse]:
    service = get_scenario_service(db)
    scenario = service.update_scenario(project_id, scenario_id, payload, current_user)
    return success_response(ScenarioResponse.model_validate(scenario))


@router.post("/{project_id}/scenarios/{scenario_id}/duplicate", response_model=ApiResponse[ScenarioResponse])
def duplicate_scenario(
    project_id: UUID,
    scenario_id: UUID,
    payload: ScenarioDuplicateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioResponse]:
    service = get_scenario_service(db)
    scenario = service.duplicate_scenario(project_id, scenario_id, payload, current_user)
    return success_response(ScenarioResponse.model_validate(scenario))


@router.delete("/{project_id}/scenarios/{scenario_id}", response_model=ApiResponse[ScenarioResponse])
def delete_scenario(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioResponse]:
    service = get_scenario_service(db)
    scenario = service.delete_scenario(project_id, scenario_id, current_user)
    return success_response(ScenarioResponse.model_validate(scenario))


@router.get("/solutions/catalog", response_model=ApiResponse[list[SolutionCatalogItemResponse]])
def list_solution_catalog(
    country: str | None = None,
    family: str | None = None,
    building_type: str | None = None,
    zone_type: str | None = None,
    scope: str | None = None,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[SolutionCatalogItemResponse]]:
    service = get_scenario_service(db)
    return success_response(
        [
            _to_catalog_item_response(item)
            for item in service.list_catalog(
                current_user,
                country=country,
                family=family,
                building_type=building_type,
                zone_type=zone_type,
                scope=scope,
                include_inactive=include_inactive,
            )
        ]
    )


@router.get("/{project_id}/scenarios/{scenario_id}/solutions", response_model=ApiResponse[list[ScenarioSolutionDetailedResponse]])
def list_scenario_solutions(
    project_id: UUID,
    scenario_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ScenarioSolutionDetailedResponse]]:
    service = get_scenario_service(db)
    assignments = service.list_assignments(project_id, scenario_id, current_user)
    catalog = {item.code: item for item in service.list_catalog(current_user, include_inactive=True)}
    data = [
        _to_assignment_detail(item, catalog)
        for item in assignments
    ]
    return success_response(data)


@router.post("/{project_id}/scenarios/{scenario_id}/solutions", response_model=ApiResponse[ScenarioSolutionDetailedResponse])
def create_scenario_solution(
    project_id: UUID,
    scenario_id: UUID,
    payload: ScenarioSolutionAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioSolutionDetailedResponse]:
    service = get_scenario_service(db)
    assignment = service.create_assignment(project_id, scenario_id, payload, current_user)
    catalog = {item.code: item for item in service.list_catalog(current_user, include_inactive=True)}
    return success_response(_to_assignment_detail(assignment, catalog))


@router.patch("/{project_id}/scenarios/{scenario_id}/solutions/{assignment_id}", response_model=ApiResponse[ScenarioSolutionDetailedResponse])
def update_scenario_solution(
    project_id: UUID,
    scenario_id: UUID,
    assignment_id: UUID,
    payload: ScenarioSolutionAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioSolutionDetailedResponse]:
    service = get_scenario_service(db)
    assignment = service.update_assignment(project_id, scenario_id, assignment_id, payload, current_user)
    catalog = {item.code: item for item in service.list_catalog(current_user, include_inactive=True)}
    return success_response(_to_assignment_detail(assignment, catalog))


@router.delete("/{project_id}/scenarios/{scenario_id}/solutions/{assignment_id}", response_model=ApiResponse[ScenarioSolutionAssignmentResponse])
def delete_scenario_solution(
    project_id: UUID,
    scenario_id: UUID,
    assignment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ScenarioSolutionAssignmentResponse]:
    service = get_scenario_service(db)
    assignment = service.delete_assignment(project_id, scenario_id, assignment_id, current_user)
    return success_response(ScenarioSolutionAssignmentResponse.model_validate(assignment))


def _to_catalog_item_response(item) -> SolutionCatalogItemResponse:
    return SolutionCatalogItemResponse.model_validate(
        {
            **item.model_dump(),
            "solution_family": item.family,
        }
    )


def _to_assignment_detail(item, catalog: dict) -> ScenarioSolutionDetailedResponse:
    solution = catalog.get(item.solution_code)
    return ScenarioSolutionDetailedResponse.model_validate(
        {
            **ScenarioSolutionAssignmentResponse.model_validate(item).model_dump(),
            "solution_name": solution.name if solution is not None else item.solution_code,
            "solution_description": solution.description if solution is not None else "Inactive or archived solution",
            "solution_family": solution.family if solution is not None else "archived",
        }
    )
