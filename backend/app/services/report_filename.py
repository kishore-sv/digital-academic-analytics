"""Report download filename helpers."""

import re

from app.schemas.report import ReportFilterLabels


def _slug(text: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", text)
    cleaned = re.sub(r"[\s_]+", "-", cleaned.strip())
    return cleaned or "Report"


def build_report_filename(
    institution_name: str,
    labels: ReportFilterLabels,
    extension: str = "pdf",
) -> str:
    parts = [_slug(institution_name)]
    if labels.academic_year != "All Academic Years":
        parts.append(_slug(labels.academic_year))
    if labels.semester != "All Semesters":
        parts.append(_slug(labels.semester))
    if labels.department != "Institution":
        parts.append(_slug(labels.department))
    if labels.program != "All Programs":
        parts.append(_slug(labels.program))
    if labels.course != "All Courses":
        parts.append(_slug(labels.course))
    if labels.risk_level != "All Risk Levels":
        parts.append(_slug(labels.risk_level))
    parts.append("Academic-Report")
    return f"{'-'.join(parts)}.{extension}"
