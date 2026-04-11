from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.calculation_assumption_set import CalculationAssumptionSet
from app.db.models.calculation_run import CalculationRun


class AssumptionSetRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_visible(self, organization_id: UUID) -> list[CalculationAssumptionSet]:
        statement = (
            select(CalculationAssumptionSet)
            .where(
                (CalculationAssumptionSet.organization_id.is_(None))
                | (CalculationAssumptionSet.organization_id == organization_id)
            )
            .order_by(
                CalculationAssumptionSet.scope.asc(),
                CalculationAssumptionSet.name.asc(),
                CalculationAssumptionSet.version.asc(),
            )
        )
        return list(self.db.scalars(statement).all())

    def get_visible(
        self,
        assumption_set_id: UUID,
        organization_id: UUID,
    ) -> CalculationAssumptionSet | None:
        statement = select(CalculationAssumptionSet).where(
            CalculationAssumptionSet.id == assumption_set_id,
            (
                (CalculationAssumptionSet.organization_id.is_(None))
                | (CalculationAssumptionSet.organization_id == organization_id)
            ),
        )
        return self.db.scalar(statement)

    def get_duplicate(
        self,
        *,
        scope: str,
        version: str,
        organization_id: UUID | None,
        country_profile_id: UUID | None,
        exclude_id: UUID | None = None,
    ) -> CalculationAssumptionSet | None:
        statement = select(CalculationAssumptionSet).where(
            CalculationAssumptionSet.scope == scope,
            CalculationAssumptionSet.version == version,
        )
        if organization_id is None:
            statement = statement.where(CalculationAssumptionSet.organization_id.is_(None))
        else:
            statement = statement.where(CalculationAssumptionSet.organization_id == organization_id)
        if country_profile_id is None:
            statement = statement.where(CalculationAssumptionSet.country_profile_id.is_(None))
        else:
            statement = statement.where(
                CalculationAssumptionSet.country_profile_id == country_profile_id
            )
        if exclude_id is not None:
            statement = statement.where(CalculationAssumptionSet.id != exclude_id)
        return self.db.scalar(statement)

    def create(self, **kwargs: object) -> CalculationAssumptionSet:
        assumption_set = CalculationAssumptionSet(**kwargs)
        self.db.add(assumption_set)
        self.db.commit()
        self.db.refresh(assumption_set)
        return assumption_set

    def update(
        self,
        assumption_set: CalculationAssumptionSet,
        **kwargs: object,
    ) -> CalculationAssumptionSet:
        for field, value in kwargs.items():
            setattr(assumption_set, field, value)
        self.db.add(assumption_set)
        self.db.commit()
        self.db.refresh(assumption_set)
        return assumption_set

    def deactivate_active_for_scope(
        self,
        *,
        scope: str,
        organization_id: UUID | None,
        country_profile_id: UUID | None,
        except_id: UUID,
    ) -> None:
        for item in self.list_active_for_scope(
            scope=scope,
            organization_id=organization_id,
            country_profile_id=country_profile_id,
        ):
            if item.id != except_id:
                item.is_active = False
                self.db.add(item)
        self.db.flush()

    def list_active_for_scope(
        self,
        *,
        scope: str,
        organization_id: UUID | None,
        country_profile_id: UUID | None,
    ) -> list[CalculationAssumptionSet]:
        statement = select(CalculationAssumptionSet).where(
            CalculationAssumptionSet.scope == scope,
            CalculationAssumptionSet.is_active.is_(True),
        )
        if organization_id is None:
            statement = statement.where(CalculationAssumptionSet.organization_id.is_(None))
        else:
            statement = statement.where(CalculationAssumptionSet.organization_id == organization_id)
        if country_profile_id is None:
            statement = statement.where(CalculationAssumptionSet.country_profile_id.is_(None))
        else:
            statement = statement.where(
                CalculationAssumptionSet.country_profile_id == country_profile_id
            )
        return list(self.db.scalars(statement).all())

    def count_historical_uses(self, assumption_set: CalculationAssumptionSet) -> int:
        runs = self.db.scalars(select(CalculationRun)).all()
        return sum(
            1 for run in runs if _run_uses_assumption_set(run.input_snapshot, assumption_set)
        )


def _run_uses_assumption_set(
    input_snapshot: dict,
    assumption_set: CalculationAssumptionSet,
) -> bool:
    assumptions = input_snapshot.get("assumptions", {}) if isinstance(input_snapshot, dict) else {}
    if not isinstance(assumptions, dict):
        return False
    if assumptions.get("assumption_set_id") == str(assumption_set.id):
        return True
    return (
        assumptions.get("assumption_set_version") == assumption_set.version
        and assumptions.get("assumption_set_scope") == assumption_set.scope
    )
