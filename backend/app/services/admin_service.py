from uuid import UUID

from app.core.exceptions import BusinessRuleError, ForbiddenError, NotFoundError, ValidationError
from app.core.security import get_password_hash
from app.repositories.branding_repository import BrandingRepository
from app.repositories.user_repository import UserRepository


class AdminService:
    ADMIN_ROLES = {"org_admin"}

    def __init__(self, user_repository: UserRepository, branding_repository: BrandingRepository):
        self.user_repository = user_repository
        self.branding_repository = branding_repository

    def ensure_admin(self, current_user) -> None:
        if current_user.role not in self.ADMIN_ROLES:
            raise ForbiddenError("Admin permissions required")

    def list_users(self, current_user):
        self.ensure_admin(current_user)
        return self.user_repository.list_by_organization(current_user.organization_id)

    def create_user(self, payload, current_user):
        self.ensure_admin(current_user)
        existing = self.user_repository.get_by_email(payload.email)
        if existing is not None:
            raise ValidationError("Validation failed", field="email", details={"reason": "email already exists"})

        return self.user_repository.create(
            organization_id=current_user.organization_id,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role=payload.role,
            preferred_language=payload.preferred_language,
            is_active=True,
        )

    def deactivate_user(self, user_id: UUID, current_user):
        self.ensure_admin(current_user)
        if user_id == current_user.id:
            raise BusinessRuleError("Cannot deactivate your own account")

        user = self.user_repository.get_by_id(user_id)
        if user is None or user.organization_id != current_user.organization_id:
            raise NotFoundError("User not found")
        return self.user_repository.update(user, is_active=False)

    def list_branding_profiles(self, current_user):
        self.ensure_admin(current_user)
        return self.branding_repository.list_for_organization(current_user.organization_id)

    def create_branding_profile(self, payload, current_user):
        self.ensure_admin(current_user)
        if payload.is_default:
            self._clear_default_branding(current_user.organization_id)
        return self.branding_repository.create(
            organization_id=current_user.organization_id,
            **payload.model_dump(),
        )

    def update_branding_profile(self, profile_id: UUID, payload, current_user):
        self.ensure_admin(current_user)
        profile = self.branding_repository.get_by_id(profile_id, current_user.organization_id)
        if profile is None:
            raise NotFoundError("Branding profile not found")

        updates = payload.model_dump(exclude_unset=True)
        if updates.get("is_default"):
            self._clear_default_branding(current_user.organization_id, except_profile_id=profile.id)
        if not updates:
            return profile
        return self.branding_repository.update(profile, **updates)

    def _clear_default_branding(self, organization_id, except_profile_id=None) -> None:
        profiles = self.branding_repository.list_for_organization(organization_id)
        for profile in profiles:
            if except_profile_id is not None and profile.id == except_profile_id:
                continue
            if profile.is_default:
                self.branding_repository.update(profile, is_default=False)
