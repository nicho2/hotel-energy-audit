from app.core.exceptions import NotFoundError
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository, branding_repo: BrandingRepository):
        self.repo = repo
        self.branding_repo = branding_repo

    def create_project(self, payload, current_user):
        branding_profile_id = self._resolve_branding_profile_id(
            payload.branding_profile_id,
            current_user.organization_id,
        )
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
            branding_profile_id=branding_profile_id,
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
        if "branding_profile_id" in updates:
            updates["branding_profile_id"] = self._resolve_branding_profile_id(
                updates["branding_profile_id"],
                current_user.organization_id,
            )
        return self.repo.update(project, **updates)

    def _resolve_branding_profile_id(self, branding_profile_id, organization_id):
        if branding_profile_id is None:
            return None
        branding_profile = self.branding_repo.get_by_id(branding_profile_id, organization_id)
        if branding_profile is None:
            raise NotFoundError("Branding profile not found")
        return branding_profile.id
