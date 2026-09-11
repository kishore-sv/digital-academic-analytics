"""Shared helpers for v1 API routes."""

import uuid
from typing import TypeVar

from app.core.tenant import get_tenant_entity
from app.schemas.common import PaginationParams
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

T = TypeVar("T")


def pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(page=page, limit=limit)


PaginationDep = Depends(pagination_params)


def get_entity_or_404(
    db: Session,
    model: type[T],
    entity_id: uuid.UUID,
    institution_id: uuid.UUID,
    detail: str | None = None,
) -> T:
    entity = get_tenant_entity(db, model, entity_id, institution_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or f"{model.__name__} not found",
        )
    return entity


def parse_uuid(value: str, field: str = "id") -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {field}",
        )
