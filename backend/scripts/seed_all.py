from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.session import SessionLocal

DEV_ORGANIZATION_SLUG = "demo-org"
DEV_USER_EMAIL = "demo@hotel-energy-audit.example.com"
DEV_USER_PASSWORD = "admin1234"


def seed_dev_auth_data() -> None:
    with SessionLocal() as db:
        organization = db.scalar(select(Organization).where(Organization.slug == DEV_ORGANIZATION_SLUG))
        if organization is None:
            organization = Organization(
                name="Demo Organization",
                slug=DEV_ORGANIZATION_SLUG,
                default_language="fr",
                is_active=True,
            )
            db.add(organization)
            db.flush()

        user = db.scalar(select(User).where(User.email == DEV_USER_EMAIL))
        if user is None:
            user = User(
                organization_id=organization.id,
                email=DEV_USER_EMAIL,
                password_hash=get_password_hash(DEV_USER_PASSWORD),
                first_name="Demo",
                last_name="User",
                role="org_admin",
                preferred_language="fr",
                is_active=True,
            )
            db.add(user)
        else:
            user.organization_id = organization.id
            user.password_hash = get_password_hash(DEV_USER_PASSWORD)
            user.first_name = "Demo"
            user.last_name = "User"
            user.role = "org_admin"
            user.preferred_language = "fr"
            user.is_active = True

        db.commit()


def main() -> None:
    seed_dev_auth_data()
    print("Seed complete.")
    print(f"Dev user email: {DEV_USER_EMAIL}")
    print(f"Dev user password: {DEV_USER_PASSWORD}")


if __name__ == "__main__":
    main()
