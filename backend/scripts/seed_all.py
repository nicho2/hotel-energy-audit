from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.models.bacs_function_definition import BacsFunctionDefinition
from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.session import SessionLocal

DEV_ORGANIZATION_SLUG = "demo-org"
DEV_USER_EMAIL = "demo@hotel-energy-audit.example.com"
DEV_USER_PASSWORD = "admin1234"

BACS_FUNCTION_DEFINITIONS_V1 = [
    {
        "code": "monitoring.central_supervision",
        "domain": "monitoring",
        "name": "Central supervision platform",
        "description": "A central platform supervises major technical equipment and provides a consolidated view.",
        "weight": 12.0,
        "order_index": 1,
    },
    {
        "code": "monitoring.alarm_reporting",
        "domain": "monitoring",
        "name": "Alarm and fault reporting",
        "description": "The site receives structured alarms for technical faults and can react quickly.",
        "weight": 8.0,
        "order_index": 2,
    },
    {
        "code": "heating.schedule_control",
        "domain": "heating",
        "name": "Heating schedules",
        "description": "Heating operation follows planned schedules adapted to occupancy periods.",
        "weight": 10.0,
        "order_index": 1,
    },
    {
        "code": "heating.zone_control",
        "domain": "heating",
        "name": "Heating zone control",
        "description": "Heating is controlled by zone or functional area instead of one uniform setting.",
        "weight": 8.0,
        "order_index": 2,
    },
    {
        "code": "cooling_ventilation.cooling_schedule",
        "domain": "cooling_ventilation",
        "name": "Cooling schedules",
        "description": "Cooling systems are scheduled according to occupancy and operating periods.",
        "weight": 10.0,
        "order_index": 1,
    },
    {
        "code": "cooling_ventilation.ventilation_demand_control",
        "domain": "cooling_ventilation",
        "name": "Demand-controlled ventilation",
        "description": "Ventilation adapts to occupancy or indoor air quality signals.",
        "weight": 10.0,
        "order_index": 2,
    },
    {
        "code": "dhw.schedule_control",
        "domain": "dhw",
        "name": "DHW schedules",
        "description": "Domestic hot water production is scheduled according to building use patterns.",
        "weight": 8.0,
        "order_index": 1,
    },
    {
        "code": "dhw.temperature_optimization",
        "domain": "dhw",
        "name": "DHW temperature optimization",
        "description": "Hot water production temperature is optimized while keeping service constraints.",
        "weight": 6.0,
        "order_index": 2,
    },
    {
        "code": "lighting.schedule_control",
        "domain": "lighting",
        "name": "Lighting schedules",
        "description": "Lighting follows schedules in common spaces and back-of-house areas.",
        "weight": 8.0,
        "order_index": 1,
    },
    {
        "code": "lighting.occupancy_control",
        "domain": "lighting",
        "name": "Occupancy-based lighting control",
        "description": "Lighting in relevant spaces reacts to presence detection or room status.",
        "weight": 10.0,
        "order_index": 2,
    },
]


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

        for definition_data in BACS_FUNCTION_DEFINITIONS_V1:
            definition = db.scalar(
                select(BacsFunctionDefinition).where(
                    BacsFunctionDefinition.code == definition_data["code"]
                )
            )
            if definition is None:
                definition = BacsFunctionDefinition(version="v1", is_active=True, **definition_data)
                db.add(definition)
            else:
                definition.domain = definition_data["domain"]
                definition.name = definition_data["name"]
                definition.description = definition_data["description"]
                definition.weight = definition_data["weight"]
                definition.order_index = definition_data["order_index"]
                definition.version = "v1"
                definition.is_active = True

        db.commit()


def main() -> None:
    seed_dev_auth_data()
    print("Seed complete.")
    print(f"Dev user email: {DEV_USER_EMAIL}")
    print(f"Dev user password: {DEV_USER_PASSWORD}")


if __name__ == "__main__":
    main()
