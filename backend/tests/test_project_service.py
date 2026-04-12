from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.exceptions import NotFoundError
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService


class _FakeProjectRepository:
    def __init__(self) -> None:
        self.created_kwargs = None

    def create(self, **kwargs):
        self.created_kwargs = kwargs
        return SimpleNamespace(id=uuid4(), **kwargs)

    def get_by_id(self, project_id, organization_id):
        return SimpleNamespace(
            id=project_id,
            organization_id=organization_id,
            branding_profile_id=None,
            name="Existing Project",
        )

    def update(self, project, **updates):
        for key, value in updates.items():
            setattr(project, key, value)
        return project


class _FakeBrandingRepository:
    def __init__(self, available_branding_id=None) -> None:
        self.available_branding_id = available_branding_id

    def get_by_id(self, branding_profile_id, organization_id):
        if branding_profile_id == self.available_branding_id:
            return SimpleNamespace(id=branding_profile_id, organization_id=organization_id)
        return None


def test_create_project_rejects_unknown_branding_profile() -> None:
    service = ProjectService(_FakeProjectRepository(), _FakeBrandingRepository())
    current_user = SimpleNamespace(id=uuid4(), organization_id=uuid4())

    payload = ProjectCreate(
        name="Demo Project",
        building_type="hotel",
        project_goal="reduce_energy",
        country_profile_id=uuid4(),
        climate_zone_id=uuid4(),
        branding_profile_id=uuid4(),
    )

    with pytest.raises(NotFoundError, match="Branding profile not found"):
        service.create_project(payload, current_user)


def test_create_project_passes_resolved_branding_profile_id_to_repository() -> None:
    branding_profile_id = uuid4()
    country_profile_id = uuid4()
    climate_zone_id = uuid4()
    project_repo = _FakeProjectRepository()
    service = ProjectService(project_repo, _FakeBrandingRepository(branding_profile_id))
    current_user = SimpleNamespace(id=uuid4(), organization_id=uuid4())

    payload = ProjectCreate(
        name="Demo Project",
        building_type="hotel",
        project_goal="reduce_energy",
        country_profile_id=country_profile_id,
        climate_zone_id=climate_zone_id,
        branding_profile_id=branding_profile_id,
    )

    created = service.create_project(payload, current_user)

    assert created.branding_profile_id == branding_profile_id
    assert project_repo.created_kwargs["branding_profile_id"] == branding_profile_id
    assert project_repo.created_kwargs["country_profile_id"] == country_profile_id
    assert project_repo.created_kwargs["climate_zone_id"] == climate_zone_id


def test_update_project_without_changes_returns_existing_project() -> None:
    service = ProjectService(_FakeProjectRepository(), _FakeBrandingRepository())
    current_user = SimpleNamespace(id=uuid4(), organization_id=uuid4())
    project_id = uuid4()

    project = service.update_project(project_id, ProjectUpdate(), current_user)

    assert project.id == project_id
    assert project.name == "Existing Project"
