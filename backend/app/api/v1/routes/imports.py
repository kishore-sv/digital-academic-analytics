"""Master data bulk import API."""

import uuid

from app.api.deps import AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.import_constants import IMPORT_TYPES, canonical_fields
from app.models.import_job import ImportJob
from app.models.user import User
from app.schemas.common import PaginatedResponse, PaginationParams
from app.schemas.import_job import (
    ImportCommitRequest,
    ImportJobResponse,
    ImportJobSummaryResponse,
    ImportMappingUpdate,
    ImportPreviewResponse,
    ImportUploadResponse,
    ImportValidationResult,
)
from app.services.import_job_service import (
    build_template_csv,
    build_template_xlsx,
    commit_job,
    create_job_from_upload,
    errors_csv,
    import_summary,
    preview_job,
    validate_job,
)
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response

router = APIRouter(prefix="/imports", tags=["imports"])


def _job_response(db: DbSession, job: ImportJob) -> ImportJobResponse:
    email = None
    if job.uploaded_by_id:
        user = db.query(User).filter(User.id == job.uploaded_by_id).first()
        email = user.email if user else None
    return ImportJobResponse(
        id=str(job.id),
        import_type=job.import_type,
        filename=job.filename,
        status=job.status,
        total_rows=job.total_rows,
        valid_rows=job.valid_rows,
        invalid_rows=job.invalid_rows,
        duplicate_rows=job.duplicate_rows,
        created_rows=job.created_rows,
        failed_rows=job.failed_rows,
        error_summary=job.error_summary,
        uploaded_by_email=email,
        created_at=job.created_at,
    )


def _get_job(db: DbSession, job_id: str, institution_id: uuid.UUID) -> ImportJob:
    return get_entity_or_404(
        db, ImportJob, parse_uuid(job_id, "job_id"), institution_id
    )


@router.get("/summary", response_model=ImportJobSummaryResponse)
def get_import_summary(current: AdminUser, db: DbSession):
    return ImportJobSummaryResponse(**import_summary(db, current.institution_id))


@router.get("/jobs", response_model=PaginatedResponse[ImportJobResponse])
def list_import_jobs(
    current: AdminUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(ImportJob)
        .filter(ImportJob.institution_id == current.institution_id)
        .order_by(ImportJob.created_at.desc())
    )
    items, meta = paginate(query, params)

    def serialize(job: ImportJob) -> ImportJobResponse:
        return _job_response(db, job)

    return paginated_response(items, meta, serialize)


@router.get("/jobs/{job_id}", response_model=ImportJobResponse)
def get_import_job(job_id: str, current: AdminUser, db: DbSession):
    job = _get_job(db, job_id, current.institution_id)
    return _job_response(db, job)


@router.post("/jobs", response_model=ImportUploadResponse)
async def upload_import_job(
    current: AdminUser,
    db: DbSession,
    file: UploadFile = File(...),
    import_type: str = Form(...),
):
    if import_type not in IMPORT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Import type '{import_type}' is not available.",
        )
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file.")
    try:
        job, headers = create_job_from_upload(
            db,
            institution_id=current.institution_id,
            user_id=current.user.id,
            import_type=import_type,
            filename=file.filename or "upload.csv",
            content=content,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return ImportUploadResponse(
        job_id=str(job.id),
        filename=job.filename,
        detected_headers=headers,
        suggested_mapping=job.column_mapping or {},
        canonical_fields=canonical_fields(import_type),
        row_count=job.total_rows,
    )


@router.patch("/jobs/{job_id}/mapping")
def update_import_mapping(
    job_id: str,
    body: ImportMappingUpdate,
    current: AdminUser,
    db: DbSession,
):
    job = _get_job(db, job_id, current.institution_id)
    job.column_mapping = body.column_mapping
    job.status = "mapped"
    db.commit()
    return {"ok": True}


@router.post("/jobs/{job_id}/validate", response_model=ImportValidationResult)
def validate_import_job(job_id: str, current: AdminUser, db: DbSession):
    job = _get_job(db, job_id, current.institution_id)
    try:
        errors = validate_job(db, job)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return ImportValidationResult(
        total_rows=job.total_rows,
        valid_rows=job.valid_rows,
        invalid_rows=job.invalid_rows,
        duplicate_rows=job.duplicate_rows,
        errors=errors,
    )


@router.get("/jobs/{job_id}/preview", response_model=ImportPreviewResponse)
def preview_import_job(job_id: str, current: AdminUser, db: DbSession):
    job = _get_job(db, job_id, current.institution_id)
    if job.status not in ("validated", "committed", "completed_with_errors"):
        try:
            validate_job(db, job)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    data = preview_job(job)
    return ImportPreviewResponse(**data)


@router.post("/jobs/{job_id}/commit", response_model=ImportJobResponse)
def commit_import_job(
    job_id: str,
    body: ImportCommitRequest,
    current: AdminUser,
    db: DbSession,
):
    job = _get_job(db, job_id, current.institution_id)
    try:
        commit_job(db, job, current.institution_id, body.duplicate_mode)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return _job_response(db, job)


@router.get("/jobs/{job_id}/errors.csv")
def download_import_errors(job_id: str, current: AdminUser, db: DbSession):
    job = _get_job(db, job_id, current.institution_id)
    return Response(
        content=errors_csv(job),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="import-{job_id}-errors.csv"'},
    )


@router.get("/types/{import_type}/template.csv")
def download_template_csv(import_type: str, current: AdminUser):
    if import_type not in IMPORT_TYPES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown import type")
    return Response(
        content=build_template_csv(import_type),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{import_type}-template.csv"'},
    )


@router.get("/types/{import_type}/template.xlsx")
def download_template_xlsx(import_type: str, current: AdminUser):
    if import_type not in IMPORT_TYPES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown import type")
    try:
        content = build_template_xlsx(import_type)
    except ImportError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="XLSX templates require openpyxl on the server.",
        )
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{import_type}-template.xlsx"'},
    )
