"""Tenant-scoped query helpers."""

import uuid
from typing import TypeVar

from fastapi import HTTPException, status
from sqlalchemy.orm import Query, Session

T = TypeVar("T")


def tenant_filter(query: Query[T], model: type, institution_id: uuid.UUID) -> Query[T]:
    """Apply institution_id filter to a SQLAlchemy query."""
    return query.filter(model.institution_id == institution_id)


def get_tenant_entity(
    db: Session,
    model: type[T],
    entity_id: uuid.UUID,
    institution_id: uuid.UUID,
) -> T | None:
    """Fetch a single tenant-owned entity or return None."""
    return (
        db.query(model)
        .filter(model.id == entity_id, model.institution_id == institution_id)
        .first()
    )


def assert_same_institution(
    entity_institution_id: uuid.UUID,
    current_institution_id: uuid.UUID,
    detail: str = "Access denied",
) -> None:
    """Raise 403 if entity does not belong to the current tenant."""
    if entity_institution_id != current_institution_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
