from sqlalchemy import delete, select

from app.db.models.bacs_assessment import BacsAssessment
from app.db.models.building import Building
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.session import SessionLocal
from scripts.demo_seed_data import DEMO_PROJECT_REFERENCE_CODES
from scripts.seed_all import DEV_ORGANIZATION_SLUG, seed_demo_showcase_data, seed_dev_auth_data


def _clear_demo_projects() -> None:
    with SessionLocal() as db:
        organization = db.scalar(select(Organization).where(Organization.slug == DEV_ORGANIZATION_SLUG))
        if organization is None:
            return
        project_ids = db.scalars(
            select(Project.id).where(
                Project.organization_id == organization.id,
                Project.reference_code.in_(DEMO_PROJECT_REFERENCE_CODES),
            )
        ).all()
        if not project_ids:
            return
        db.execute(delete(BacsAssessment).where(BacsAssessment.project_id.in_(project_ids)))
        db.execute(delete(Building).where(Building.project_id.in_(project_ids)))
        db.execute(delete(Project).where(Project.id.in_(project_ids)))
        db.commit()


def test_seed_demo_showcase_creates_three_ready_projects() -> None:
    _clear_demo_projects()
    seed_dev_auth_data()
    seed_demo_showcase_data()
    seed_demo_showcase_data()

    with SessionLocal() as db:
        organization = db.scalar(select(Organization).where(Organization.slug == DEV_ORGANIZATION_SLUG))
        assert organization is not None

        projects = db.scalars(
            select(Project).where(
                Project.organization_id == organization.id,
                Project.reference_code.in_(DEMO_PROJECT_REFERENCE_CODES),
            )
        ).all()

        assert len(projects) == 3
        assert {project.reference_code for project in projects} == set(DEMO_PROJECT_REFERENCE_CODES)
        assert {project.building_type for project in projects} == {"hotel", "residence"}
        assert {
            project.reference_code: project.name
            for project in projects
        } == {
            "DEMO-HOTEL-001": "Hotel Lumiere Paris",
            "DEMO-HOTEL-SW-001": "Hotel Belvedere Sud-Ouest",
            "DEMO-RESIDENCE-001": "Residence Azur Seaside",
        }
        for project in projects:
            assert project.status == "ready"
            assert project.wizard_step == 10
            assert project.building is not None
            assert len(project.zones) >= 3
            assert len(project.technical_systems) >= 3
            assert len(project.scenarios) == 2
            assert len(project.calculation_runs) == 2

    _clear_demo_projects()
