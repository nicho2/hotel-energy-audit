from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.db.models.branding_profile import BrandingProfile
from app.db.models.organization import Organization
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


def test_list_branding_profiles_returns_current_organization_profiles(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Organization",
            slug=f"other-branding-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        visible_default = BrandingProfile(
            organization_id=user["organization_id"],
            name="Default",
            company_name="Visible Default",
            accent_color="#14365d",
            logo_text="VD",
            is_default=True,
        )
        visible_secondary = BrandingProfile(
            organization_id=user["organization_id"],
            name="Secondary",
            company_name="Visible Secondary",
            accent_color="#166534",
            logo_text="VS",
            is_default=False,
        )
        hidden = BrandingProfile(
            organization_id=other_organization.id,
            name="Hidden",
            company_name="Hidden Brand",
            accent_color="#b91c1c",
            logo_text="HB",
            is_default=True,
        )
        db.add_all([visible_default, visible_secondary, hidden])
        db.commit()

    response = client.get(
        "/api/v1/branding",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    names = [profile["company_name"] for profile in body["data"]]
    assert names == ["Visible Default", "Visible Secondary"]
    assert "Hidden Brand" not in names
