from sqlalchemy.orm import Session
from app.db.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Project:
        project = Project(**kwargs)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id, organization_id) -> Project | None:
        return (
            self.db.query(Project)
            .filter(Project.id == project_id, Project.organization_id == organization_id)
            .first()
        )

    def list(self, organization_id) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(Project.organization_id == organization_id)
            .order_by(Project.updated_at.desc())
            .all()
        )
