from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.db.models.branding_profile import BrandingProfile
from app.db.models.user import User
from app.db.session import SessionLocal
from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient, email: str = DEV_USER_EMAIL, password: str = DEV_USER_PASSWORD) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    body = response.json()
    return body["data"]["access_token"], body["data"]["user"]


def test_admin_can_list_create_and_deactivate_users(client: TestClient) -> None:
    token, _user = _login(client)
    email = f"new-admin-user-{uuid4().hex[:8]}@example.com"

    create_response = client.post(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": email,
            "password": "password123",
            "first_name": "New",
            "last_name": "User",
            "role": "member",
            "preferred_language": "en",
        },
    )

    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["email"] == email
    assert created["is_active"] is True
    assert "password_hash" not in created

    list_response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    assert email in {user["email"] for user in list_response.json()["data"]}

    deactivate_response = client.post(
        f"/api/v1/admin/users/{created['id']}/deactivate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["data"]["is_active"] is False


def test_admin_branding_create_update_and_default_switch(client: TestClient) -> None:
    token, _user = _login(client)

    create_response = client.post(
        "/api/v1/admin/branding",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Default brand",
            "company_name": "Legrand Hospitality",
            "accent_color": "#14365d",
            "logo_text": "LH",
            "contact_email": "contact@example.com",
            "is_default": True,
        },
    )

    assert create_response.status_code == 200
    profile = create_response.json()["data"]
    assert profile["is_default"] is True

    update_response = client.patch(
        f"/api/v1/admin/branding/{profile['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={"company_name": "Legrand Hotels", "accent_color": "#166534"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["company_name"] == "Legrand Hotels"
    assert update_response.json()["data"]["accent_color"] == "#166534"


def test_non_admin_is_forbidden_from_admin_endpoints(client: TestClient) -> None:
    _token, admin_user = _login(client)
    email = f"member-{uuid4().hex[:8]}@example.com"

    with SessionLocal() as db:
        user = User(
            organization_id=admin_user["organization_id"],
            email=email,
            password_hash=get_password_hash("password123"),
            first_name="Member",
            last_name="User",
            role="member",
            preferred_language="fr",
            is_active=True,
        )
        db.add(user)
        db.commit()

    member_token, _member = _login(client, email, "password123")
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert response.status_code == 403


def test_admin_branding_list_is_scoped_to_current_organization(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        visible = BrandingProfile(
            organization_id=user["organization_id"],
            name="Visible",
            company_name="Visible Brand",
            accent_color="#14365d",
            logo_text="VB",
            is_default=True,
        )
        db.add(visible)
        db.commit()

    response = client.get(
        "/api/v1/admin/branding",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert [profile["company_name"] for profile in response.json()["data"]] == ["Visible Brand"]
