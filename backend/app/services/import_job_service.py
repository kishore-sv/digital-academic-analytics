"""Import job validation, preview, and commit orchestration."""

from __future__ import annotations

import csv
import io
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.import_constants import (
    AVAILABLE_MASTER_IMPORT_COUNT,
    AVAILABLE_OPERATIONAL_IMPORT_COUNT,
    COMING_SOON_IMPORT_COUNT,
    IMPORT_TYPES,
    TEMPLATE_EXAMPLE_ROWS,
    canonical_fields,
    is_operational,
    suggest_column_mapping,
)
from app.models.import_job import ImportJob
from app.services.import_commit_service import commit_master_import
from app.services.import_file_service import parse_upload
from app.services.import_operational_commit import commit_operational_import
from app.services.import_operational_validation import validate_operational_row


def apply_mapping(
    rows: list[dict[str, str]], mapping: dict[str, str]
) -> list[dict[str, str]]:
    mapped: list[dict[str, str]] = []
    for row in rows:
        out: dict[str, str] = {}
        for header, value in row.items():
            target = mapping.get(header)
            if target:
                out[target] = value
        mapped.append(out)
    return mapped


def validate_job(db: Session, job: ImportJob) -> list[dict[str, Any]]:
    cfg = IMPORT_TYPES.get(job.import_type)
    if not cfg:
        raise ValueError(f"Unsupported import type: {job.import_type}")
    if not job.raw_rows or not job.column_mapping:
        raise ValueError("Import job is missing file data or column mapping.")

    mapped = apply_mapping(job.raw_rows, job.column_mapping)
    errors: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    duplicate_rows = 0

    for idx, row in enumerate(mapped, start=2):
        row_errors: list[str] = []
        for field in cfg["required"]:
            if not str(row.get(field, "")).strip():
                row_errors.append(f"Missing required field '{field}'.")

        dup_key = _duplicate_key(job.import_type, row)
        if dup_key:
            if dup_key in seen_keys:
                duplicate_rows += 1
                row_errors.append("Duplicate row in file.")
            else:
                seen_keys.add(dup_key)

        if is_operational(job.import_type) and not row_errors:
            row_errors.extend(
                validate_operational_row(
                    db, job.institution_id, job.import_type, row
                )
            )

        for msg in row_errors:
            errors.append({"row": idx, "message": msg})

    valid_rows = len(mapped) - len({e["row"] for e in errors})
    job.total_rows = len(mapped)
    job.invalid_rows = len({e["row"] for e in errors})
    job.valid_rows = max(0, job.total_rows - job.invalid_rows)
    job.duplicate_rows = duplicate_rows
    job.row_errors = errors
    job.status = "validated"
    db.commit()
    db.refresh(job)
    return errors


def preview_job(job: ImportJob) -> dict[str, Any]:
    mapped = apply_mapping(job.raw_rows or [], job.column_mapping or {})
    error_rows = {e["row"] for e in (job.row_errors or [])}
    valid = [r for i, r in enumerate(mapped, start=2) if i not in error_rows]
    sample = valid[:5]
    return {
        "total_rows": job.total_rows,
        "valid_rows": job.valid_rows,
        "invalid_rows": job.invalid_rows,
        "duplicate_rows": job.duplicate_rows,
        "will_create": job.valid_rows,
        "sample_rows": sample,
    }


def commit_job(
    db: Session,
    job: ImportJob,
    institution_id: uuid.UUID,
    duplicate_mode: str,
) -> None:
    if job.status not in ("validated", "committed"):
        validate_job(db, job)
    mapped = apply_mapping(job.raw_rows or [], job.column_mapping or {})
    error_rows = {e["row"] for e in (job.row_errors or [])}
    valid_rows = [
        (i, r) for i, r in enumerate(mapped, start=2) if i not in error_rows
    ]
    if is_operational(job.import_type):
        created, failed = commit_operational_import(
            db,
            job.import_type,
            institution_id,
            valid_rows,
            duplicate_mode=duplicate_mode,
        )
    else:
        created, failed = commit_master_import(
            db,
            job.import_type,
            institution_id,
            valid_rows,
            duplicate_mode=duplicate_mode,
        )
    job.created_rows = created
    job.failed_rows = failed
    job.status = "committed" if failed == 0 else "completed_with_errors"
    db.commit()
    db.refresh(job)


def errors_csv(job: ImportJob) -> bytes:
    buf = io.StringIO()
    mapped = apply_mapping(job.raw_rows or [], job.column_mapping or {})
    fieldnames = list({k for row in mapped for k in row.keys()})
    headers = ["row", "message", *fieldnames]
    writer = csv.DictWriter(buf, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    for err in job.row_errors or []:
        row_num = err.get("row", "")
        row_data: dict[str, str] = {"row": row_num, "message": err.get("message", "")}
        if isinstance(row_num, int) and 2 <= row_num <= len(mapped) + 1:
            row_data.update(mapped[row_num - 2])
        writer.writerow(row_data)
    return buf.getvalue().encode("utf-8")


def build_template_csv(import_type: str) -> bytes:
    fields = canonical_fields(import_type)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(fields)
    example = TEMPLATE_EXAMPLE_ROWS.get(import_type)
    if example:
        writer.writerow([example.get(f, "") for f in fields])
    return buf.getvalue().encode("utf-8")


def build_template_xlsx(import_type: str) -> bytes:
    import pandas as pd

    fields = canonical_fields(import_type)
    example = TEMPLATE_EXAMPLE_ROWS.get(import_type)
    rows = [example] if example else []
    df = pd.DataFrame(rows, columns=fields)
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()


def create_job_from_upload(
    db: Session,
    *,
    institution_id: uuid.UUID,
    user_id: uuid.UUID,
    import_type: str,
    filename: str,
    content: bytes,
) -> tuple[ImportJob, list[str]]:
    if import_type not in IMPORT_TYPES:
        raise ValueError(f"Import type '{import_type}' is not available.")
    headers, rows = parse_upload(filename, content)
    mapping = suggest_column_mapping(import_type, headers)
    job = ImportJob(
        institution_id=institution_id,
        uploaded_by_id=user_id,
        import_type=import_type,
        filename=filename,
        status="uploaded",
        column_mapping=mapping,
        raw_rows=rows,
        total_rows=len(rows),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job, headers


def import_summary(db: Session, institution_id: uuid.UUID) -> dict[str, Any]:
    from sqlalchemy import func

    q = db.query(ImportJob).filter(ImportJob.institution_id == institution_id)
    total = q.count()
    last = (
        db.query(func.max(ImportJob.created_at))
        .filter(ImportJob.institution_id == institution_id)
        .scalar()
    )
    return {
        "available_import_count": (
            AVAILABLE_MASTER_IMPORT_COUNT + AVAILABLE_OPERATIONAL_IMPORT_COUNT
        ),
        "coming_soon_import_count": COMING_SOON_IMPORT_COUNT,
        "total_imports": total,
        "last_import_at": last,
    }


def _duplicate_key(import_type: str, row: dict[str, str]) -> str | None:
    def g(key: str) -> str:
        return str(row.get(key, "")).strip().lower()

    match import_type:
        case "departments":
            return g("code") or None
        case "programs":
            return g("code") or None
        case "academic_years":
            return g("name") or None
        case "semesters":
            if g("academic_year_name") and g("number"):
                return f"{g('academic_year_name')}:{g('number')}"
            return None
        case "courses":
            return g("code") or None
        case "program_courses":
            if g("program_code") and g("course_code"):
                return f"{g('program_code')}:{g('course_code')}"
            return None
        case "batches":
            return g("code") or None
        case "class_groups":
            if g("batch_code") and g("code"):
                return f"{g('batch_code')}:{g('code')}"
            return None
        case "sections":
            if g("class_code") and g("code"):
                return f"{g('class_code')}:{g('code')}"
            return None
        case "faculty":
            return g("employee_id") or None
        case "students":
            return g("roll_number") or None
        case "parents":
            return g("email") or None
        case "enrollments":
            parts = [g("student_roll_number"), g("course_code"), g("academic_year_name"), g("semester_number")]
            if all(parts):
                return ":".join(parts)
            return None
        case "faculty_courses":
            parts = [
                g("employee_id"),
                g("course_code"),
                g("academic_year_name"),
                g("semester_number"),
                g("section_code"),
            ]
            if parts[0] and parts[1] and parts[2] and parts[3]:
                return ":".join(parts)
            return None
        case "attendance":
            parts = [
                g("student_roll_number"),
                g("course_code"),
                g("academic_year_name"),
                g("semester_number"),
                g("attendance_date"),
            ]
            if all(parts):
                return ":".join(parts)
            return None
        case "ca_marks" | "mid_term_marks" | "end_sem_marks":
            parts = [
                g("student_roll_number"),
                g("course_code"),
                g("academic_year_name"),
                g("semester_number"),
                g("assessment_name") or _marks_type_key(import_type),
                g("obtained_marks"),
            ]
            if parts[0] and parts[1] and parts[2] and parts[3] and parts[5]:
                return ":".join(parts)
            return None
        case "semester_results":
            if g("course_code"):
                return ":".join(
                    [
                        g("student_roll_number"),
                        g("academic_year_name"),
                        g("semester_number"),
                        g("course_code"),
                    ]
                )
            return ":".join(
                [
                    g("student_roll_number"),
                    g("academic_year_name"),
                    g("semester_number"),
                    "semester",
                ]
            )
        case "backlogs":
            parts = [
                g("student_roll_number"),
                g("course_code"),
                g("original_academic_year"),
                g("original_semester_number"),
            ]
            if all(parts):
                return ":".join(parts)
            return None
        case "backlog_clearance":
            parts = [
                g("student_roll_number"),
                g("course_code"),
                g("original_academic_year"),
                g("original_semester_number"),
                "clearance",
            ]
            if parts[0] and parts[1] and parts[2] and parts[3]:
                return ":".join(parts)
            return None
    return None


def _marks_type_key(import_type: str) -> str:
    return {
        "ca_marks": "ca",
        "mid_term_marks": "mid",
        "end_sem_marks": "final",
    }.get(import_type, "mark")
