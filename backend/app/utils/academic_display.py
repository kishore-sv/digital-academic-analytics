"""Academic display helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.semester import Semester


def format_year_number(year_number: int) -> str:
    """Format year of study as ordinal label (e.g. 3 -> '3rd Year')."""
    if year_number < 1:
        return f"Year {year_number}"
    suffix = "th"
    if year_number % 100 not in (11, 12, 13):
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(year_number % 10, "th")
    return f"{year_number}{suffix} Year"


def semester_year_number(semester_number: int) -> int:
    """Derive year of study from degree semester number (2 semesters per year)."""
    return max(1, (semester_number + 1) // 2)


def semester_is_after(candidate: Semester, current: Semester | None) -> bool:
    """Return True when candidate is chronologically after current semester."""
    if current is None:
        return True
    if candidate.academic_year_id == current.academic_year_id:
        return candidate.number > current.number
    candidate_year = candidate.academic_year.name if candidate.academic_year else ""
    current_year = current.academic_year.name if current.academic_year else ""
    if candidate_year != current_year:
        return candidate_year > current_year
    return candidate.number > current.number
