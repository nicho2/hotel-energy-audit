from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs: object) -> Project:
        project = Project(**kwargs)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: UUID, organization_id: UUID) -> Project | None:
        statement = select(Project).where(
            Project.id == project_id,
            Project.organization_id == organization_id,
        )
        return self.db.scalar(statement)

    def list(self, organization_id: UUID) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.organization_id == organization_id)
            .order_by(Project.updated_at.desc())
        )
        return list(self.db.scalars(statement).all())

    def update(self, project: Project, **kwargs: object) -> Project:
        for field, value in kwargs.items():
            setattr(project, field, value)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
