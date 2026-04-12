from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.project_template import ProjectTemplate


class ProjectTemplateRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_organization(
        self,
        organization_id: UUID,
        *,
        include_inactive: bool = False,
    ) -> list[ProjectTemplate]:
        statement = (
            select(ProjectTemplate)
            .where(ProjectTemplate.organization_id == organization_id)
            .order_by(ProjectTemplate.updated_at.desc(), ProjectTemplate.name.asc())
        )
        if not include_inactive:
            statement = statement.where(ProjectTemplate.is_active.is_(True))
        return list(self.db.scalars(statement).all())

    def get_by_id(self, template_id: UUID, organization_id: UUID) -> ProjectTemplate | None:
        statement = select(ProjectTemplate).where(
            ProjectTemplate.id == template_id,
            ProjectTemplate.organization_id == organization_id,
        )
        return self.db.scalar(statement)

    def get_by_name(self, name: str, organization_id: UUID) -> ProjectTemplate | None:
        statement = select(ProjectTemplate).where(
            ProjectTemplate.name == name,
            ProjectTemplate.organization_id == organization_id,
        )
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> ProjectTemplate:
        template = ProjectTemplate(**kwargs)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def update(self, template: ProjectTemplate, **kwargs: object) -> ProjectTemplate:
        for field, value in kwargs.items():
            setattr(template, field, value)
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template
