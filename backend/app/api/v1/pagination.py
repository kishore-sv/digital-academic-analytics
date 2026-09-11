"""Pagination utilities."""

import math

from app.schemas.common import PaginatedResponse, PaginationMeta, PaginationParams
from sqlalchemy.orm import Query


def paginate(query: Query, params: PaginationParams) -> tuple[list, PaginationMeta]:
    total = query.count()
    total_pages = max(1, math.ceil(total / params.limit)) if total else 0
    offset = (params.page - 1) * params.limit
    items = query.offset(offset).limit(params.limit).all()
    meta = PaginationMeta(
        page=params.page,
        limit=params.limit,
        total=total,
        total_pages=total_pages,
    )
    return items, meta


def paginated_response(items: list, meta: PaginationMeta, serializer):
    if callable(serializer):
        data = [serializer(item) for item in items]
    else:
        data = [serializer.model_validate(item) for item in items]
    return PaginatedResponse(data=data, meta=meta)
