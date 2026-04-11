from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models.solution_catalog import SolutionCatalog
from app.db.models.solution_definition import SolutionDefinition


class SolutionCatalogRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_catalogs(self, organization_id: UUID) -> list[SolutionCatalog]:
        statement = (
            select(SolutionCatalog)
            .where((SolutionCatalog.organization_id.is_(None)) | (SolutionCatalog.organization_id == organization_id))
            .order_by(SolutionCatalog.scope.asc(), SolutionCatalog.name.asc(), SolutionCatalog.version.asc())
        )
        return list(self.db.scalars(statement).all())

    def get_catalog(self, catalog_id: UUID, organization_id: UUID) -> SolutionCatalog | None:
        statement = select(SolutionCatalog).where(
            SolutionCatalog.id == catalog_id,
            (SolutionCatalog.organization_id.is_(None)) | (SolutionCatalog.organization_id == organization_id),
        )
        return self.db.scalar(statement)

    def get_catalog_by_scope(
        self,
        *,
        scope: str,
        version: str,
        organization_id: UUID | None,
        country_code: str | None,
    ) -> SolutionCatalog | None:
        statement = select(SolutionCatalog).where(
            SolutionCatalog.scope == scope,
            SolutionCatalog.version == version,
        )
        statement = statement.where(
            SolutionCatalog.organization_id.is_(None)
            if organization_id is None
            else SolutionCatalog.organization_id == organization_id
        )
        statement = statement.where(
            SolutionCatalog.country_code.is_(None)
            if country_code is None
            else SolutionCatalog.country_code == country_code
        )
        return self.db.scalar(statement)

    def create_catalog(self, **kwargs: object) -> SolutionCatalog:
        catalog = SolutionCatalog(**kwargs)
        self.db.add(catalog)
        self.db.commit()
        self.db.refresh(catalog)
        return catalog

    def list_solutions(self, organization_id: UUID, *, include_inactive: bool = False) -> list[SolutionDefinition]:
        statement = (
            select(SolutionDefinition)
            .join(SolutionDefinition.catalog)
            .where((SolutionCatalog.organization_id.is_(None)) | (SolutionCatalog.organization_id == organization_id))
            .options(joinedload(SolutionDefinition.catalog))
            .order_by(SolutionDefinition.priority.asc(), SolutionDefinition.code.asc())
        )
        if not include_inactive:
            statement = statement.where(
                SolutionDefinition.is_active.is_(True),
                SolutionCatalog.is_active.is_(True),
            )
        return list(self.db.scalars(statement).all())

    def get_solution_by_id(self, solution_id: UUID, organization_id: UUID) -> SolutionDefinition | None:
        statement = (
            select(SolutionDefinition)
            .join(SolutionDefinition.catalog)
            .where(
                SolutionDefinition.id == solution_id,
                (SolutionCatalog.organization_id.is_(None)) | (SolutionCatalog.organization_id == organization_id),
            )
            .options(joinedload(SolutionDefinition.catalog))
        )
        return self.db.scalar(statement)

    def get_solution_by_code(
        self,
        code: str,
        organization_id: UUID,
        *,
        include_inactive: bool = False,
    ) -> SolutionDefinition | None:
        statement = (
            select(SolutionDefinition)
            .join(SolutionDefinition.catalog)
            .where(
                SolutionDefinition.code == code,
                (SolutionCatalog.organization_id.is_(None)) | (SolutionCatalog.organization_id == organization_id),
            )
            .options(joinedload(SolutionDefinition.catalog))
        )
        if not include_inactive:
            statement = statement.where(
                SolutionDefinition.is_active.is_(True),
                SolutionCatalog.is_active.is_(True),
            )
        return self.db.scalar(statement)

    def create_solution(self, **kwargs: object) -> SolutionDefinition:
        solution = SolutionDefinition(**kwargs)
        self.db.add(solution)
        self.db.commit()
        self.db.refresh(solution)
        return solution

    def update_solution(self, solution: SolutionDefinition, **kwargs: object) -> SolutionDefinition:
        for field, value in kwargs.items():
            setattr(solution, field, value)
        self.db.add(solution)
        self.db.commit()
        self.db.refresh(solution)
        return solution
