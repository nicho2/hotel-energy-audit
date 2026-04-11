from uuid import UUID

from app.core.exceptions import BusinessRuleError, ForbiddenError, NotFoundError, ValidationError
from app.repositories.assumption_set_repository import AssumptionSetRepository
from app.schemas.assumption_sets import (
    AssumptionSetCloneRequest,
    AssumptionSetCreate,
    AssumptionSetResponse,
    AssumptionSetUpdate,
    validate_assumption_json_payloads,
    validate_scope,
)

LOCKED_FIELDS = {
    "name",
    "version",
    "scope",
    "country_profile_id",
    "heating_model_json",
    "cooling_model_json",
    "ventilation_model_json",
    "dhw_model_json",
    "lighting_model_json",
    "auxiliaries_model_json",
    "economic_defaults_json",
    "bacs_rules_json",
    "co2_factors_json",
}


class AssumptionSetService:
    ADMIN_ROLES = {"org_admin"}

    def __init__(self, repository: AssumptionSetRepository, audit_service=None):
        self.repository = repository
        self.audit_service = audit_service

    def ensure_admin(self, current_user) -> None:
        if current_user.role not in self.ADMIN_ROLES:
            raise ForbiddenError("Admin permissions required")

    def list_assumption_sets(self, current_user) -> list[AssumptionSetResponse]:
        self.ensure_admin(current_user)
        items = self.repository.list_visible(current_user.organization_id)
        return [self._to_response(item) for item in items]

    def get_assumption_set(self, assumption_set_id: UUID, current_user) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        item = self._get_visible_or_404(assumption_set_id, current_user)
        return self._to_response(item)

    def create_assumption_set(
        self,
        payload: AssumptionSetCreate,
        current_user,
    ) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        data = payload.model_dump()
        data["organization_id"] = (
            current_user.organization_id if payload.scope == "organization_override" else None
        )
        self._ensure_unique(data)
        if data["is_active"]:
            self.repository.deactivate_active_for_scope(
                scope=data["scope"],
                organization_id=data["organization_id"],
                country_profile_id=data["country_profile_id"],
                except_id=UUID(int=0),
            )
        item = self.repository.create(**data)
        return self._to_response(item)

    def update_assumption_set(
        self,
        assumption_set_id: UUID,
        payload: AssumptionSetUpdate,
        current_user,
    ) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        item = self._get_visible_or_404(assumption_set_id, current_user)
        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return self._to_response(item)

        used_count = self.repository.count_historical_uses(item)
        locked_updates = LOCKED_FIELDS.intersection(updates)
        if used_count > 0 and locked_updates:
            raise BusinessRuleError(
                (
                    "Assumption set is used by historical calculations; "
                    "clone it before changing assumptions"
                ),
                details={
                    "historical_calculation_count": used_count,
                    "locked_fields": sorted(locked_updates),
                    "recommended_action": "clone",
                },
            )

        merged = self._merged_payload(item, updates, current_user.organization_id)
        self._validate_payload(merged)
        self._ensure_unique(merged, exclude_id=item.id)

        if updates.get("is_active"):
            self.repository.deactivate_active_for_scope(
                scope=merged["scope"],
                organization_id=merged["organization_id"],
                country_profile_id=merged["country_profile_id"],
                except_id=item.id,
            )
        update_data = dict(updates)
        if "scope" in updates:
            update_data["organization_id"] = merged["organization_id"]
            update_data["country_profile_id"] = merged["country_profile_id"]
        before_json = _assumption_set_audit_payload(item)
        updated = self.repository.update(item, **update_data)
        self._audit_assumption_set(
            action="assumption_set_updated",
            item=updated,
            current_user=current_user,
            before_json=before_json,
            after_json=_assumption_set_audit_payload(updated, changed_fields=sorted(updates)),
        )
        return self._to_response(updated)

    def clone_assumption_set(
        self,
        assumption_set_id: UUID,
        payload: AssumptionSetCloneRequest,
        current_user,
    ) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        source = self._get_visible_or_404(assumption_set_id, current_user)
        scope = payload.scope or source.scope
        country_profile_id = (
            payload.country_profile_id if payload.scope is not None else source.country_profile_id
        )
        organization_id = current_user.organization_id if scope == "organization_override" else None
        clone_data = {
            "organization_id": organization_id,
            "country_profile_id": country_profile_id,
            "cloned_from_id": source.id,
            "name": payload.name or f"{source.name} copy",
            "version": payload.version,
            "scope": scope,
            "heating_model_json": dict(source.heating_model_json),
            "cooling_model_json": dict(source.cooling_model_json),
            "ventilation_model_json": dict(source.ventilation_model_json),
            "dhw_model_json": dict(source.dhw_model_json),
            "lighting_model_json": dict(source.lighting_model_json),
            "auxiliaries_model_json": dict(source.auxiliaries_model_json),
            "economic_defaults_json": dict(source.economic_defaults_json),
            "bacs_rules_json": dict(source.bacs_rules_json),
            "co2_factors_json": dict(source.co2_factors_json),
            "notes": payload.notes if payload.notes is not None else source.notes,
            "is_active": payload.is_active,
        }
        self._validate_payload(clone_data)
        self._ensure_unique(clone_data)
        if clone_data["is_active"]:
            self.repository.deactivate_active_for_scope(
                scope=clone_data["scope"],
                organization_id=clone_data["organization_id"],
                country_profile_id=clone_data["country_profile_id"],
                except_id=UUID(int=0),
            )
        clone = self.repository.create(**clone_data)
        return self._to_response(clone)

    def activate_assumption_set(
        self,
        assumption_set_id: UUID,
        current_user,
    ) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        item = self._get_visible_or_404(assumption_set_id, current_user)
        before_json = _assumption_set_audit_payload(item)
        self.repository.deactivate_active_for_scope(
            scope=item.scope,
            organization_id=item.organization_id,
            country_profile_id=item.country_profile_id,
            except_id=item.id,
        )
        updated = self.repository.update(item, is_active=True)
        self._audit_assumption_set(
            action="assumption_set_updated",
            item=updated,
            current_user=current_user,
            before_json=before_json,
            after_json=_assumption_set_audit_payload(updated, changed_fields=["is_active"]),
        )
        return self._to_response(updated)

    def deactivate_assumption_set(
        self,
        assumption_set_id: UUID,
        current_user,
    ) -> AssumptionSetResponse:
        self.ensure_admin(current_user)
        item = self._get_visible_or_404(assumption_set_id, current_user)
        before_json = _assumption_set_audit_payload(item)
        updated = self.repository.update(item, is_active=False)
        self._audit_assumption_set(
            action="assumption_set_updated",
            item=updated,
            current_user=current_user,
            before_json=before_json,
            after_json=_assumption_set_audit_payload(updated, changed_fields=["is_active"]),
        )
        return self._to_response(updated)

    def _audit_assumption_set(
        self,
        *,
        action: str,
        item,
        current_user,
        before_json: dict | None = None,
        after_json: dict | None = None,
    ) -> None:
        if self.audit_service is not None:
            self.audit_service.log(
                entity_type="calculation_assumption_set",
                entity_id=item.id,
                action=action,
                current_user=current_user,
                before_json=before_json,
                after_json=after_json,
            )

    def _get_visible_or_404(self, assumption_set_id: UUID, current_user):
        item = self.repository.get_visible(assumption_set_id, current_user.organization_id)
        if item is None:
            raise NotFoundError("Assumption set not found")
        return item

    def _to_response(self, item) -> AssumptionSetResponse:
        used_count = self.repository.count_historical_uses(item)
        return AssumptionSetResponse(
            id=item.id,
            organization_id=item.organization_id,
            country_profile_id=item.country_profile_id,
            cloned_from_id=item.cloned_from_id,
            name=item.name,
            version=item.version,
            scope=item.scope,
            heating_model_json=item.heating_model_json,
            cooling_model_json=item.cooling_model_json,
            ventilation_model_json=item.ventilation_model_json,
            dhw_model_json=item.dhw_model_json,
            lighting_model_json=item.lighting_model_json,
            auxiliaries_model_json=item.auxiliaries_model_json,
            economic_defaults_json=item.economic_defaults_json,
            bacs_rules_json=item.bacs_rules_json,
            co2_factors_json=item.co2_factors_json,
            notes=item.notes,
            is_active=item.is_active,
            is_locked=used_count > 0,
            historical_calculation_count=used_count,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    def _merged_payload(self, item, updates: dict, organization_id: UUID) -> dict:
        scope = updates.get("scope", item.scope)
        country_profile_id = updates.get("country_profile_id", item.country_profile_id)
        if (
            "scope" in updates
            and scope != "country_default"
            and "country_profile_id" not in updates
        ):
            country_profile_id = None
        return {
            "organization_id": organization_id if scope == "organization_override" else None,
            "country_profile_id": country_profile_id,
            "name": updates.get("name", item.name),
            "version": updates.get("version", item.version),
            "scope": scope,
            "heating_model_json": updates.get("heating_model_json", item.heating_model_json),
            "cooling_model_json": updates.get("cooling_model_json", item.cooling_model_json),
            "ventilation_model_json": updates.get(
                "ventilation_model_json",
                item.ventilation_model_json,
            ),
            "dhw_model_json": updates.get("dhw_model_json", item.dhw_model_json),
            "lighting_model_json": updates.get("lighting_model_json", item.lighting_model_json),
            "auxiliaries_model_json": updates.get(
                "auxiliaries_model_json",
                item.auxiliaries_model_json,
            ),
            "economic_defaults_json": updates.get(
                "economic_defaults_json",
                item.economic_defaults_json,
            ),
            "bacs_rules_json": updates.get("bacs_rules_json", item.bacs_rules_json),
            "co2_factors_json": updates.get("co2_factors_json", item.co2_factors_json),
            "notes": updates.get("notes", item.notes),
            "is_active": updates.get("is_active", item.is_active),
        }

    def _validate_payload(self, data: dict) -> None:
        try:
            validate_scope(data["scope"], data["country_profile_id"])
            validate_assumption_json_payloads(data)
        except ValueError as exc:
            raise ValidationError("Validation failed", details={"reason": str(exc)}) from exc

    def _ensure_unique(self, data: dict, exclude_id: UUID | None = None) -> None:
        duplicate = self.repository.get_duplicate(
            scope=data["scope"],
            version=data["version"],
            organization_id=data["organization_id"],
            country_profile_id=data["country_profile_id"],
            exclude_id=exclude_id,
        )
        if duplicate is not None:
            raise ValidationError(
                "Validation failed",
                field="version",
                details={"reason": "version already exists for this scope"},
            )


def _assumption_set_audit_payload(item, *, changed_fields: list[str] | None = None) -> dict:
    data = {
        "id": item.id,
        "name": item.name,
        "version": item.version,
        "scope": item.scope,
        "country_profile_id": item.country_profile_id,
        "organization_id": item.organization_id,
        "is_active": item.is_active,
        "notes": item.notes,
    }
    if changed_fields is not None:
        data["changed_fields"] = changed_fields
    return data
