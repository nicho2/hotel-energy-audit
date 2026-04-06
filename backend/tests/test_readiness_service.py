from types import SimpleNamespace
from uuid import uuid4

from app.services.readiness_service import ReadinessService


class _StaticProjectService:
    def get_project(self, project_id, current_user):
        return SimpleNamespace(id=project_id, organization_id=current_user.organization_id)


class _StaticBuildingRepository:
    def __init__(self, building):
        self.building = building

    def get_by_project_id(self, project_id):
        return self.building


class _StaticZoneRepository:
    def __init__(self, zones):
        self.zones = zones

    def list_by_project_id(self, project_id):
        return self.zones


class _StaticTechnicalSystemRepository:
    def __init__(self, systems):
        self.systems = systems

    def list_by_project_id(self, project_id):
        return self.systems


def test_get_calculation_readiness_reports_missing_blockers_and_low_confidence() -> None:
    service = ReadinessService(
        project_service=_StaticProjectService(),
        building_repository=_StaticBuildingRepository(None),
        zone_repository=_StaticZoneRepository([]),
        technical_system_repository=_StaticTechnicalSystemRepository([]),
    )

    response = service.get_calculation_readiness(uuid4(), SimpleNamespace(organization_id=uuid4()))

    assert response.is_ready is False
    assert response.confidence_level == "low"
    assert [issue.code for issue in response.blocking_issues] == [
        "building_missing",
        "zones_missing",
    ]
    assert [issue.code for issue in response.warnings] == [
        "heating_system_missing",
        "dhw_system_missing",
        "reference_scenario_implicit",
    ]


def test_get_calculation_readiness_returns_high_confidence_for_complete_project() -> None:
    service = ReadinessService(
        project_service=_StaticProjectService(),
        building_repository=_StaticBuildingRepository(SimpleNamespace(name="Hotel Demo")),
        zone_repository=_StaticZoneRepository([SimpleNamespace(name="Rooms")]),
        technical_system_repository=_StaticTechnicalSystemRepository(
            [
                SimpleNamespace(system_type="heating"),
                SimpleNamespace(system_type="dhw"),
            ]
        ),
    )

    response = service.get_calculation_readiness(uuid4(), SimpleNamespace(organization_id=uuid4()))

    assert response.is_ready is True
    assert response.blocking_issues == []
    assert response.confidence_level == "high"
    assert [issue.code for issue in response.warnings] == ["reference_scenario_implicit"]
