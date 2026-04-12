from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.models.branding_profile import BrandingProfile
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.user import User
from app.db.session import SessionLocal
from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    return body["data"]["access_token"], body["data"]["user"]


def test_create_project_returns_created_project_for_current_organization(client: TestClient) -> None:
    token, user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()

    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Lumiere",
            "client_name": "Groupe Lumiere",
            "reference_code": "HL-001",
            "description": "Projet pilote",
            "country_profile_id": str(country_profile_id),
            "climate_zone_id": str(climate_zone_id),
            "building_type": "hotel",
            "project_goal": "reduce_energy",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert body["data"]["name"] == "Hotel Lumiere"
    assert body["data"]["organization_id"] == user["organization_id"]
    assert body["data"]["created_by_user_id"] == user["id"]
    assert body["data"]["wizard_step"] == 1
    assert body["data"]["status"] == "draft"
    assert body["data"]["country_profile_id"] == str(country_profile_id)
    assert body["data"]["climate_zone_id"] == str(climate_zone_id)


def test_project_country_and_climate_fields_roundtrip_create_get_list(client: TestClient) -> None:
    token, _user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()

    create_response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Roundtrip Project",
            "building_type": "hotel",
            "project_goal": "reduce_energy",
            "country_profile_id": str(country_profile_id),
            "climate_zone_id": str(climate_zone_id),
        },
    )
    assert create_response.status_code == 200
    created = create_response.json()["data"]

    get_response = client.get(
        f"/api/v1/projects/{created['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_response.status_code == 200
    fetched = get_response.json()["data"]
    assert fetched["country_profile_id"] == str(country_profile_id)
    assert fetched["climate_zone_id"] == str(climate_zone_id)

    list_response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    projects_by_id = {project["id"]: project for project in list_response.json()["data"]}
    assert projects_by_id[created["id"]]["country_profile_id"] == str(country_profile_id)
    assert projects_by_id[created["id"]]["climate_zone_id"] == str(climate_zone_id)


def test_create_project_requires_country_and_climate_context(client: TestClient) -> None:
    token, _user = _login(client)

    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Missing Context Project",
            "building_type": "hotel",
            "project_goal": "reduce_energy",
        },
    )

    assert response.status_code == 422
    body = response.json()
    fields = {error["field"] for error in body["errors"]}
    assert fields == {"country_profile_id", "climate_zone_id"}


def test_list_projects_only_returns_projects_for_current_organization(client: TestClient) -> None:
    token, user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()
    visible_project_name = f"Visible Project {uuid4().hex[:8]}"
    hidden_project_name = f"Hidden Project {uuid4().hex[:8]}"

    with SessionLocal() as db:
        current_user = db.scalar(select(User).where(User.id == user["id"]))
        assert current_user is not None

        other_organization = Organization(
            name="Other Organization",
            slug=f"other-org-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        other_user = User(
            organization_id=other_organization.id,
            email=f"other-{uuid4().hex[:8]}@example.com",
            password_hash=get_password_hash("password123"),
            first_name="Other",
            last_name="User",
            role="org_admin",
            preferred_language="fr",
            is_active=True,
        )
        db.add(other_user)
        db.flush()

        db.add_all(
            [
                Project(
                    organization_id=current_user.organization_id,
                    created_by_user_id=current_user.id,
                    name=visible_project_name,
                    country_profile_id=country_profile_id,
                    climate_zone_id=climate_zone_id,
                    building_type="hotel",
                    project_goal="baseline",
                ),
                Project(
                    organization_id=other_organization.id,
                    created_by_user_id=other_user.id,
                    name=hidden_project_name,
                    building_type="hotel",
                    project_goal="baseline",
                ),
            ]
        )
        db.commit()

    response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    projects_by_name = {project["name"]: project for project in body["data"]}
    project_names = set(projects_by_name)
    assert visible_project_name in project_names
    assert hidden_project_name not in project_names
    assert projects_by_name[visible_project_name]["country_profile_id"] == str(country_profile_id)
    assert projects_by_name[visible_project_name]["climate_zone_id"] == str(climate_zone_id)


def test_get_project_returns_only_project_from_current_organization(client: TestClient) -> None:
    token, user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Project Detail",
            country_profile_id=country_profile_id,
            climate_zone_id=climate_zone_id,
            building_type="hotel",
            project_goal="compare_scenarios",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == project_id
    assert body["data"]["name"] == "Project Detail"
    assert body["data"]["country_profile_id"] == str(country_profile_id)
    assert body["data"]["climate_zone_id"] == str(climate_zone_id)


def test_patch_project_updates_partial_fields(client: TestClient) -> None:
    token, user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Original Name",
            client_name="Client A",
            country_profile_id=uuid4(),
            climate_zone_id=uuid4(),
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Name",
            "wizard_step": 3,
            "description": "Updated description",
            "country_profile_id": str(country_profile_id),
            "climate_zone_id": str(climate_zone_id),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["name"] == "Updated Name"
    assert body["data"]["wizard_step"] == 3
    assert body["data"]["description"] == "Updated description"
    assert body["data"]["client_name"] == "Client A"
    assert body["data"]["country_profile_id"] == str(country_profile_id)
    assert body["data"]["climate_zone_id"] == str(climate_zone_id)


def test_create_project_persists_branding_profile_id(client: TestClient) -> None:
    token, user = _login(client)
    country_profile_id = uuid4()
    climate_zone_id = uuid4()

    with SessionLocal() as db:
        branding_profile = BrandingProfile(
            organization_id=user["organization_id"],
            name="Default brand",
            company_name="Legrand Hospitality",
            accent_color="#ff5a1f",
            logo_text="LG",
            contact_email="sales@legrand.example.com",
            is_default=True,
        )
        db.add(branding_profile)
        db.commit()
        db.refresh(branding_profile)

    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Branded Project",
            "building_type": "hotel",
            "project_goal": "reduce_energy",
            "country_profile_id": str(country_profile_id),
            "climate_zone_id": str(climate_zone_id),
            "branding_profile_id": str(branding_profile.id),
        },
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["branding_profile_id"] == str(branding_profile.id)
