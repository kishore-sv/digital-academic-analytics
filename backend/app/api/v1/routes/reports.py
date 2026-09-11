"""Report generation routes."""

import uuid

from app.api.deps import AdminOrFacultyUser, AdminUser, CurrentUserDep, DbSession
from app.api.v1.analytics_filters import AnalyticsFilterParams, analytics_filter_dep
from app.schemas.report import ReportContext
from app.services.analytics_aggregations import get_scoped_ids
from app.services.authorization_service import assert_student_access
from app.services.report_data_service import build_report_context
from app.services.report_filename import build_report_filename
from app.services.pdf_service import render_pdf
from app.services.report_service import (
    generate_at_risk_report,
    generate_institutional_report,
    generate_student_prediction_report,
)
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse, Response

router = APIRouter(prefix="/reports", tags=["reports"])


def _render_pdf(html: str, filename: str) -> Response:
    try:
        pdf = render_pdf(html)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/institutional/data", response_model=ReportContext)
def institutional_report_data(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return build_report_context(db, current.institution_id, filters)


@router.get("/scoped/institutional/data", response_model=ReportContext)
def scoped_institutional_report_data(
    current: AdminOrFacultyUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return build_report_context(db, current.institution_id, filters, scope_ids)


@router.get("/institutional")
def institutional_report(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
    include_charts: bool = Query(False),
):
    html = generate_institutional_report(
        db,
        current.institution_id,
        filters=filters,
        include_charts=include_charts,
    )
    return HTMLResponse(content=html)


@router.get("/institutional/pdf")
def institutional_report_pdf(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
    include_charts: bool = Query(True),
):
    context = build_report_context(db, current.institution_id, filters)
    html = generate_institutional_report(
        db,
        current.institution_id,
        filters=filters,
        include_charts=include_charts,
    )
    filename = build_report_filename(context.header.institution_name, context.header.filters)
    return _render_pdf(html, filename)


@router.get("/scoped/institutional/pdf")
def scoped_institutional_report_pdf(
    current: AdminOrFacultyUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
    include_charts: bool = Query(True),
):
    scope_ids = get_scoped_ids(db, current.user)
    context = build_report_context(db, current.institution_id, filters, scope_ids)
    html = generate_institutional_report(
        db,
        current.institution_id,
        filters=filters,
        include_charts=include_charts,
        scope_ids=scope_ids,
    )
    filename = build_report_filename(context.header.institution_name, context.header.filters)
    return _render_pdf(html, filename)


@router.get("/at-risk")
def at_risk_report(
    current: AdminOrFacultyUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
    include_charts: bool = Query(False),
):
    scope_ids = get_scoped_ids(db, current.user)
    html = generate_at_risk_report(
        db,
        current.institution_id,
        filters=filters,
        include_charts=include_charts,
        scope_ids=scope_ids,
    )
    return HTMLResponse(content=html)


@router.get("/at-risk/pdf")
def at_risk_report_pdf(
    current: AdminOrFacultyUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
    include_charts: bool = Query(True),
):
    scope_ids = get_scoped_ids(db, current.user)
    context = build_report_context(db, current.institution_id, filters, scope_ids)
    html = generate_at_risk_report(
        db,
        current.institution_id,
        filters=filters,
        include_charts=include_charts,
        scope_ids=scope_ids,
    )
    filename = build_report_filename(
        context.header.institution_name,
        context.header.filters,
    ).replace("Academic-Report", "At-Risk-Report")
    return _render_pdf(html, filename)


@router.get("/student/{student_id}")
def student_prediction_report(
    student_id: str,
    current: CurrentUserDep,
    db: DbSession,
):
    student_uuid = uuid.UUID(student_id)
    assert_student_access(db, current.user, student_uuid)
    try:
        html = generate_student_prediction_report(
            db, current.institution_id, student_uuid
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return HTMLResponse(content=html)
