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

    response = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Hotel Lumiere",
            "client_name": "Groupe Lumiere",
            "reference_code": "HL-001",
            "description": "Projet pilote",
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


def test_list_projects_only_returns_projects_for_current_organization(client: TestClient) -> None:
    token, user = _login(client)

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
                    name="Visible Project",
                    building_type="hotel",
                    project_goal="baseline",
                ),
                Project(
                    organization_id=other_organization.id,
                    created_by_user_id=other_user.id,
                    name="Hidden Project",
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
    project_names = {project["name"] for project in body["data"]}
    assert "Visible Project" in project_names
    assert "Hidden Project" not in project_names


def test_get_project_returns_only_project_from_current_organization(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Project Detail",
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


def test_patch_project_updates_partial_fields(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Original Name",
            client_name="Client A",
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
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["name"] == "Updated Name"
    assert body["data"]["wizard_step"] == 3
    assert body["data"]["description"] == "Updated description"
    assert body["data"]["client_name"] == "Client A"


def test_create_project_persists_branding_profile_id(client: TestClient) -> None:
    token, user = _login(client)

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
            "branding_profile_id": str(branding_profile.id),
        },
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["branding_profile_id"] == str(branding_profile.id)
