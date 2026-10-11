"""Import job API schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class ImportJobSummaryResponse(BaseModel):
    available_import_count: int
    coming_soon_import_count: int
    total_imports: int
    last_import_at: datetime | None = None


class ImportJobResponse(BaseModel):
    id: str
    import_type: str
    filename: str
    status: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    created_rows: int
    failed_rows: int
    error_summary: str | None = None
    uploaded_by_email: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ImportUploadResponse(BaseModel):
    job_id: str
    filename: str
    detected_headers: list[str]
    suggested_mapping: dict[str, str]
    canonical_fields: list[str]
    row_count: int


class ImportMappingUpdate(BaseModel):
    column_mapping: dict[str, str]


class ImportValidationResult(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    errors: list[dict[str, str | int]]


class ImportPreviewResponse(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    will_create: int
    sample_rows: list[dict[str, str]]


class ImportCommitRequest(BaseModel):
    duplicate_mode: str = Field(default="reject", pattern="^(reject|skip)$")
