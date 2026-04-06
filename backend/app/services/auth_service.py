from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, verify_password
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("User account is inactive")
        return user

    def login(self, email: str, password: str) -> LoginResponse:
        user = self.authenticate(email, password)
        token = create_access_token(
            str(user.id),
            organization_id=str(user.organization_id),
            email=user.email,
            role=user.role,
        )
        return LoginResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=user,
        )
