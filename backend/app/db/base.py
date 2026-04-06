from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.db.models.organization import Organization  # noqa: E402,F401
from app.db.models.project import Project  # noqa: E402,F401
from app.db.models.user import User  # noqa: E402,F401
