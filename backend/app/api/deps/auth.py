from fastapi import Depends, Header
from sqlalchemy.orm import Session
from app.api.deps.db import get_db
from app.db.models.user import User
from app.core.exceptions import UnauthorizedError


def get_current_user(
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
) -> User:
    # Placeholder for MVP bootstrap.
    user = db.query(User).first()
    if not user:
        raise UnauthorizedError("No user found. Seed at least one user.")
    return user
