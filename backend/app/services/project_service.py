from app.repositories.project_repository import ProjectRepository
from app.core.exceptions import NotFoundError


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def create_project(self, payload, current_user):
        return self.repo.create(
            organization_id=current_user.organization_id,
            created_by_user_id=current_user.id,
            name=payload.name,
            client_name=payload.client_name,
            reference_code=payload.reference_code,
            description=payload.description,
            status="draft",
            wizard_step=1,
            building_type=payload.building_type,
            project_goal=payload.project_goal,
        )

    def get_project(self, project_id, current_user):
        project = self.repo.get_by_id(project_id, current_user.organization_id)
        if not project:
            raise NotFoundError("Project not found")
        return project

    def list_projects(self, current_user):
        return self.repo.list(current_user.organization_id)

    def update_project(self, project_id, payload, current_user):
        project = self.get_project(project_id, current_user)
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return project
        return self.repo.update(project, **updates)
