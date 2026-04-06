from collections import defaultdict
from dataclasses import dataclass

from app.core.exceptions import NotFoundError, ValidationError
from app.repositories.building_repository import BuildingRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.zones import ZoneValidationItem, ZoneValidationResponse
from app.services.project_service import ProjectService


@dataclass(frozen=True)
class ZoneGenerationResult:
    zones: list
    warnings: list[str]


class ZoneService:
    def __init__(
        self,
        zone_repository: ZoneRepository,
        building_repository: BuildingRepository,
        project_service: ProjectService,
    ):
        self.zone_repository = zone_repository
        self.building_repository = building_repository
        self.project_service = project_service

    def list_zones(self, project_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        return self.zone_repository.list_by_project_id(project.id)

    def create_zone(self, project_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        zone_data = payload.model_dump()
        self._validate_zone_payload(project.id, zone_data)
        return self.zone_repository.create(project_id=project.id, **zone_data)

    def update_zone(self, project_id, zone_id, payload, current_user):
        project = self.project_service.get_project(project_id, current_user)
        zone = self.zone_repository.get_by_id(zone_id, project.id)
        if zone is None:
            raise NotFoundError("Zone not found")

        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return zone

        merged = {
            "name": zone.name,
            "zone_type": zone.zone_type,
            "orientation": zone.orientation,
            "area_m2": zone.area_m2,
            "room_count": zone.room_count,
            "order_index": zone.order_index,
            **updates,
        }
        self._validate_zone_payload(project.id, merged, existing_zone_id=zone.id)
        return self.zone_repository.update(zone, **updates)

    def delete_zone(self, project_id, zone_id, current_user):
        project = self.project_service.get_project(project_id, current_user)
        zone = self.zone_repository.get_by_id(zone_id, project.id)
        if zone is None:
            raise NotFoundError("Zone not found")
        self.zone_repository.delete(zone)
        return zone

    def generate_zones(self, project_id, payload, current_user) -> ZoneGenerationResult:
        project = self.project_service.get_project(project_id, current_user)
        building = self.building_repository.get_by_project_id(project.id)
        if building is None:
            raise ValidationError(
                "Validation failed",
                field="project_id",
                details={"reason": "building is required before zone generation"},
            )

        orientation_counts: dict[str, int] = defaultdict(int)
        for item in payload.room_distribution:
            orientation_counts[item.orientation] += item.room_count

        total_rooms = sum(orientation_counts.values())
        guest_room_area_total = payload.total_guest_room_area_m2 or (
            total_rooms * payload.average_room_area_m2
        )
        warnings: list[str] = []

        zones_data: list[dict] = []
        order_index = 1
        for orientation in ("north", "east", "south", "west", "mixed"):
            room_count = orientation_counts.get(orientation, 0)
            if room_count <= 0:
                continue
            area_m2 = round(guest_room_area_total * room_count / total_rooms, 2)
            zones_data.append(
                {
                    "name": f"Guest rooms {orientation}",
                    "zone_type": "guest_rooms",
                    "orientation": orientation,
                    "area_m2": area_m2,
                    "room_count": room_count,
                    "order_index": order_index,
                }
            )
            order_index += 1

        reference_area = building.heated_area_m2 or building.gross_floor_area_m2
        remaining_area = max((reference_area or guest_room_area_total) - guest_room_area_total, 0)

        support_weights = [
            ("circulation", "Circulation", 0.35),
            ("lobby", "Lobby", 0.15),
            ("technical", "Technical", 0.10),
        ]
        if building.has_restaurant:
            support_weights.append(("restaurant", "Restaurant", 0.15))
        if building.has_meeting_rooms:
            support_weights.append(("meeting", "Meeting", 0.10))
        if building.has_spa:
            support_weights.append(("spa", "Spa", 0.10))
        if building.has_pool:
            support_weights.append(("pool", "Pool", 0.05))

        total_weight = sum(weight for _, _, weight in support_weights)
        if remaining_area <= 0:
            warnings.append("No remaining area available for support zones; only guest room zones were generated.")
        else:
            for zone_type, name, weight in support_weights:
                area_m2 = round(remaining_area * weight / total_weight, 2)
                if area_m2 <= 0:
                    continue
                zones_data.append(
                    {
                        "name": name,
                        "zone_type": zone_type,
                        "orientation": "mixed",
                        "area_m2": area_m2,
                        "room_count": 0,
                        "order_index": order_index,
                    }
                )
                order_index += 1

        if building.number_of_rooms is not None and building.number_of_rooms != total_rooms:
            warnings.append(
                "The generated room distribution does not match the building number_of_rooms."
            )

        if payload.replace_existing:
            zones = self.zone_repository.replace_for_project(project.id, zones_data)
        else:
            existing = self.zone_repository.list_by_project_id(project.id)
            start_index = max((zone.order_index for zone in existing), default=0)
            zones = existing[:]
            for index, zone_data in enumerate(zones_data, start=1):
                zone_data["order_index"] = start_index + index
                zones.append(self.zone_repository.create(project_id=project.id, **zone_data))

        return ZoneGenerationResult(zones=zones, warnings=warnings)

    def validate_zones(self, project_id, current_user) -> ZoneValidationResponse:
        project = self.project_service.get_project(project_id, current_user)
        building = self.building_repository.get_by_project_id(project.id)
        zones = self.zone_repository.list_by_project_id(project.id)

        checks: list[ZoneValidationItem] = []
        warnings: list[ZoneValidationItem] = []

        if not zones:
            checks.append(
                ZoneValidationItem(
                    code="no_zones",
                    status="error",
                    message="No zones are defined for this project.",
                )
            )
            return ZoneValidationResponse(is_valid=False, checks=checks, warnings=warnings)

        total_area = round(sum(zone.area_m2 for zone in zones), 2)
        total_rooms = sum(zone.room_count for zone in zones if zone.zone_type == "guest_rooms")

        checks.append(
            ZoneValidationItem(
                code="zones_present",
                status="ok",
                message=f"{len(zones)} zone(s) defined.",
            )
        )

        if any(zone.area_m2 <= 0 for zone in zones):
            checks.append(
                ZoneValidationItem(
                    code="zone_area_positive",
                    status="error",
                    message="All zones must have an area greater than zero.",
                )
            )
        else:
            checks.append(
                ZoneValidationItem(
                    code="zone_area_positive",
                    status="ok",
                    message="All zones have a positive area.",
                )
            )

        if any(zone.room_count < 0 for zone in zones):
            checks.append(
                ZoneValidationItem(
                    code="zone_room_count_valid",
                    status="error",
                    message="Zone room counts must be greater than or equal to zero.",
                )
            )
        else:
            checks.append(
                ZoneValidationItem(
                    code="zone_room_count_valid",
                    status="ok",
                    message="All zone room counts are valid.",
                )
            )

        reference_area = None
        if building is not None:
            reference_area = building.heated_area_m2 or building.gross_floor_area_m2

        if reference_area is None:
            warning = ZoneValidationItem(
                code="reference_area_missing",
                status="warning",
                message="Building reference area is missing; total zone area cannot be compared.",
            )
            checks.append(warning)
            warnings.append(warning)
        elif total_area > reference_area:
            checks.append(
                ZoneValidationItem(
                    code="total_area_within_building",
                    status="error",
                    message="Total zone area exceeds the building reference area.",
                )
            )
        else:
            checks.append(
                ZoneValidationItem(
                    code="total_area_within_building",
                    status="ok",
                    message="Total zone area is within the building reference area.",
                )
            )

        if building is None or building.number_of_rooms is None:
            warning = ZoneValidationItem(
                code="building_room_count_missing",
                status="warning",
                message="Building number_of_rooms is missing; guest room consistency cannot be checked.",
            )
            checks.append(warning)
            warnings.append(warning)
        elif total_rooms != building.number_of_rooms:
            warning = ZoneValidationItem(
                code="guest_room_distribution_mismatch",
                status="warning",
                message="The total guest room count in zones does not match the building number_of_rooms.",
            )
            checks.append(warning)
            warnings.append(warning)
        else:
            checks.append(
                ZoneValidationItem(
                    code="guest_room_distribution_match",
                    status="ok",
                    message="The guest room count matches the building number_of_rooms.",
                )
            )

        is_valid = not any(check.status == "error" for check in checks)
        return ZoneValidationResponse(is_valid=is_valid, checks=checks, warnings=warnings)

    def _validate_zone_payload(self, project_id, zone_data: dict, existing_zone_id=None) -> None:
        if zone_data["zone_type"] != "guest_rooms" and zone_data["room_count"] != 0:
            raise ValidationError(
                "Validation failed",
                field="room_count",
                details={"reason": "room_count must be 0 for non-guest room zones"},
            )

        zones = self.zone_repository.list_by_project_id(project_id)
        total_area = sum(zone.area_m2 for zone in zones if zone.id != existing_zone_id) + zone_data["area_m2"]
        total_rooms = sum(
            zone.room_count
            for zone in zones
            if zone.id != existing_zone_id and zone.zone_type == "guest_rooms"
        )
        if zone_data["zone_type"] == "guest_rooms":
            total_rooms += zone_data["room_count"]

        building = self.building_repository.get_by_project_id(project_id)
        if building is None:
            return

        reference_area = building.heated_area_m2 or building.gross_floor_area_m2
        if reference_area is not None and total_area > reference_area:
            raise ValidationError(
                "Validation failed",
                field="area_m2",
                details={"reason": "total zone area must be less than or equal to building reference area"},
            )

        if building.number_of_rooms is not None and total_rooms > building.number_of_rooms:
            raise ValidationError(
                "Validation failed",
                field="room_count",
                details={"reason": "total guest room count must be less than or equal to building number_of_rooms"},
            )
