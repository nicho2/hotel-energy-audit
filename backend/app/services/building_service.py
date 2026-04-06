from app.core.exceptions import ValidationError
from app.repositories.building_repository import BuildingRepository
from app.services.project_service import ProjectService


class BuildingService:
    def __init__(
        self,
        building_repository: BuildingRepository,
        project_service: ProjectService,
    ):
        self.building_repository = building_repository
        self.project_service = project_service

    def get_building(self, project_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        return self.building_repository.get_by_project_id(project.id)

    def upsert_building(self, project_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        data = payload.model_dump()
        self._validate_payload(data)

        building = self.building_repository.get_by_project_id(project.id)
        if building is None:
            return self.building_repository.create(project_id=project.id, **data)
        return self.building_repository.update(building, **data)

    @staticmethod
    def _validate_payload(data: dict) -> None:
        gross_floor_area = data.get("gross_floor_area_m2")
        heated_area = data.get("heated_area_m2")
        cooled_area = data.get("cooled_area_m2")
        number_of_floors = data.get("number_of_floors")
        number_of_rooms = data.get("number_of_rooms")

        for field in ("gross_floor_area_m2", "heated_area_m2", "cooled_area_m2"):
            value = data.get(field)
            if value is not None and value <= 0:
                raise ValidationError(
                    "Validation failed",
                    field=field,
                    details={"reason": "must be greater than zero"},
                )

        if gross_floor_area is not None and heated_area is not None and heated_area > gross_floor_area:
            raise ValidationError(
                "Validation failed",
                field="heated_area_m2",
                details={"reason": "must be less than or equal to gross_floor_area_m2"},
            )

        if gross_floor_area is not None and cooled_area is not None and cooled_area > gross_floor_area:
            raise ValidationError(
                "Validation failed",
                field="cooled_area_m2",
                details={"reason": "must be less than or equal to gross_floor_area_m2"},
            )

        if number_of_floors is not None and number_of_floors < 1:
            raise ValidationError(
                "Validation failed",
                field="number_of_floors",
                details={"reason": "must be greater than or equal to 1"},
            )

        if number_of_rooms is not None and number_of_rooms < 0:
            raise ValidationError(
                "Validation failed",
                field="number_of_rooms",
                details={"reason": "must be greater than or equal to 0"},
            )
