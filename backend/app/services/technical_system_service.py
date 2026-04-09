from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.technical_system_repository import TechnicalSystemRepository
from app.services.project_service import ProjectService


class TechnicalSystemService:
    def __init__(
        self,
        technical_system_repository: TechnicalSystemRepository,
        project_service: ProjectService,
    ):
        self.technical_system_repository = technical_system_repository
        self.project_service = project_service

    def list_systems(self, project_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        return self.technical_system_repository.list_by_project_id(project.id)

    def create_system(self, project_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        data = payload.model_dump()
        self._validate_payload(data)
        return self.technical_system_repository.create(project_id=project.id, **data)

    def update_system(self, project_id, system_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        system = self.technical_system_repository.get_by_id(system_id, project.id)
        if system is None:
            raise NotFoundError("Technical system not found")

        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return system

        merged = {
            "name": system.name,
            "system_type": system.system_type,
            "energy_source": system.energy_source,
            "technology_type": system.technology_type,
            "efficiency_level": system.efficiency_level,
            "serves": system.serves,
            "quantity": system.quantity,
            "year_installed": system.year_installed,
            "is_primary": system.is_primary,
            "notes": system.notes,
            "order_index": system.order_index,
            **updates,
        }
        self._validate_payload(merged)
        return self.technical_system_repository.update(system, **updates)

    def delete_system(self, project_id, system_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        system = self.technical_system_repository.get_by_id(system_id, project.id)
        if system is None:
            raise NotFoundError("Technical system not found")
        self.technical_system_repository.delete(system)
        return system

    @staticmethod
    def _validate_payload(data: dict) -> None:
        quantity = data.get("quantity")
        year_installed = data.get("year_installed")

        if quantity is not None and quantity < 1:
            raise ValidationError(
                "Validation failed",
                field="quantity",
                details={"reason": "must be greater than or equal to 1"},
            )

        if year_installed is not None and year_installed < 1900:
            raise ValidationError(
                "Validation failed",
                field="year_installed",
                details={"reason": "must be greater than or equal to 1900"},
            )
