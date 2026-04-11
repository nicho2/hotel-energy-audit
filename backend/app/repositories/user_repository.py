from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def list_by_organization(self, organization_id: UUID) -> list[User]:
        statement = (
            select(User)
            .where(User.organization_id == organization_id)
            .order_by(User.created_at.desc(), User.email.asc())
        )
        return list(self.db.scalars(statement).all())

    def create(self, **kwargs: object) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, **kwargs: object) -> User:
        for field, value in kwargs.items():
            setattr(user, field, value)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
