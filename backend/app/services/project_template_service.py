from uuid import UUID

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.project_template_repository import ProjectTemplateRepository
from app.repositories.reference_data_repository import ReferenceDataRepository


class ProjectTemplateService:
    def __init__(
        self,
        repository: ProjectTemplateRepository,
        reference_repository: ReferenceDataRepository,
    ):
        self.repository = repository
        self.reference_repository = reference_repository

    def list_templates(self, current_user, *, include_inactive: bool = False):
        return self.repository.list_for_organization(
            current_user.organization_id,
            include_inactive=include_inactive,
        )

    def get_template(self, template_id: UUID, current_user):
        template = self.repository.get_by_id(template_id, current_user.organization_id)
        if template is None:
            raise NotFoundError("Project template not found")
        return template

    def create_template(self, payload, current_user):
        self._ensure_country_exists(payload.country_profile_id)
        self._ensure_name_available(payload.name, current_user.organization_id)
        return self.repository.create(
            organization_id=current_user.organization_id,
            created_by_user_id=current_user.id,
            **payload.model_dump(),
        )

    def update_template(self, template_id: UUID, payload, current_user):
        template = self.get_template(template_id, current_user)
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return template
        if "country_profile_id" in updates:
            self._ensure_country_exists(updates["country_profile_id"])
        if "name" in updates and updates["name"] != template.name:
            self._ensure_name_available(updates["name"], current_user.organization_id)
        return self.repository.update(template, **updates)

    def deactivate_template(self, template_id: UUID, current_user):
        template = self.get_template(template_id, current_user)
        return self.repository.update(template, is_active=False)

    def _ensure_country_exists(self, country_profile_id: UUID) -> None:
        if self.reference_repository.get_country_profile(country_profile_id) is None:
            raise NotFoundError("Country profile not found")

    def _ensure_name_available(self, name: str, organization_id: UUID) -> None:
        if self.repository.get_by_name(name, organization_id) is not None:
            raise ValidationError(
                "Validation failed",
                field="name",
                details={"reason": "project template name already exists"},
            )
