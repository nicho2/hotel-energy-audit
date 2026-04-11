from app.core.exceptions import NotFoundError
from app.repositories.branding_repository import BrandingRepository
from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository, branding_repo: BrandingRepository, audit_service=None):
        self.repo = repo
        self.branding_repo = branding_repo
        self.audit_service = audit_service

    def create_project(self, payload, current_user):
        branding_profile_id = self._resolve_branding_profile_id(
            payload.branding_profile_id,
            current_user.organization_id,
        )
        project = self.repo.create(
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
            country_profile_id=payload.country_profile_id,
            climate_zone_id=payload.climate_zone_id,
            branding_profile_id=branding_profile_id,
        )
        self._audit(
            action="project_created",
            entity_id=project.id,
            current_user=current_user,
            after_json=_project_audit_payload(project),
            project_id=project.id,
        )
        return project

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
        before_json = _project_audit_payload(project)
        updated = self.repo.update(project, **updates)
        action = "project_archived" if updates.get("status") == "archived" else "project_updated"
        self._audit(
            action=action,
            entity_id=updated.id,
            current_user=current_user,
            before_json=before_json,
            after_json=_project_audit_payload(updated, changed_fields=sorted(updates)),
            project_id=updated.id,
        )
        return updated

    def _resolve_branding_profile_id(self, branding_profile_id, organization_id):
        if branding_profile_id is None:
            return None
        branding_profile = self.branding_repo.get_by_id(branding_profile_id, organization_id)
        if branding_profile is None:
            raise NotFoundError("Branding profile not found")
        return branding_profile.id

    def _audit(self, **kwargs) -> None:
        if self.audit_service is not None:
            self.audit_service.log(entity_type="project", **kwargs)


def _project_audit_payload(project, *, changed_fields: list[str] | None = None) -> dict:
    data = {
        "id": project.id,
        "name": project.name,
        "status": project.status,
        "building_type": project.building_type,
        "wizard_step": project.wizard_step,
        "reference_code": project.reference_code,
        "country_profile_id": project.country_profile_id,
        "climate_zone_id": project.climate_zone_id,
        "branding_profile_id": project.branding_profile_id,
    }
    if changed_fields is not None:
        data["changed_fields"] = changed_fields
    return data
