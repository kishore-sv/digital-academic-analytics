"""Master data import type definitions and column aliases."""

from __future__ import annotations

from typing import TypedDict


class ImportTypeConfig(TypedDict):
    required: list[str]
    optional: list[str]
    aliases: dict[str, list[str]]


MASTER_IMPORT_TYPES: dict[str, ImportTypeConfig] = {
    "departments": {
        "required": ["name", "code"],
        "optional": ["description"],
        "aliases": {
            "name": ["name", "department_name", "dept_name"],
            "code": ["code", "department_code", "dept_code"],
            "description": ["description", "desc"],
        },
    },
    "programs": {
        "required": ["name", "code", "department_code"],
        "optional": ["duration_semesters"],
        "aliases": {
            "name": ["name", "program_name"],
            "code": ["code", "program_code"],
            "department_code": ["department_code", "dept_code"],
            "duration_semesters": ["duration_semesters", "duration"],
        },
    },
    "academic_years": {
        "required": ["name"],
        "optional": ["is_current"],
        "aliases": {
            "name": ["name", "academic_year", "year_name"],
            "is_current": ["is_current", "current"],
        },
    },
    "semesters": {
        "required": ["academic_year_name", "number", "name", "year_number"],
        "optional": [],
        "aliases": {
            "academic_year_name": ["academic_year_name", "academic_year", "year_name"],
            "number": ["number", "semester_number", "sem_number"],
            "name": ["name", "semester_name"],
            "year_number": ["year_number", "year_of_study"],
        },
    },
    "courses": {
        "required": ["name", "code", "department_code", "credits", "course_type"],
        "optional": [],
        "aliases": {
            "name": ["name", "course_name"],
            "code": ["code", "course_code"],
            "department_code": ["department_code", "dept_code"],
            "credits": ["credits", "credit"],
            "course_type": ["course_type", "type"],
        },
    },
    "program_courses": {
        "required": ["program_code", "course_code", "semester_number"],
        "optional": [],
        "aliases": {
            "program_code": ["program_code"],
            "course_code": ["course_code"],
            "semester_number": ["semester_number", "sem_number"],
        },
    },
    "batches": {
        "required": ["program_code", "admission_year", "code", "name"],
        "optional": ["is_active"],
        "aliases": {
            "program_code": ["program_code"],
            "admission_year": ["admission_year", "batch_year", "year"],
            "code": ["code", "batch_code"],
            "name": ["name", "batch_name"],
            "is_active": ["is_active", "active"],
        },
    },
    "class_groups": {
        "required": ["batch_code", "year_number", "code", "name"],
        "optional": [],
        "aliases": {
            "batch_code": ["batch_code"],
            "year_number": ["year_number", "year_of_study"],
            "code": ["code", "class_code"],
            "name": ["name", "class_name"],
        },
    },
    "sections": {
        "required": ["class_code", "code", "name"],
        "optional": ["is_active", "batch_code"],
        "aliases": {
            "class_code": ["class_code"],
            "batch_code": ["batch_code"],
            "code": ["code", "section_code"],
            "name": ["name", "section_name"],
            "is_active": ["is_active", "active"],
        },
    },
    "faculty": {
        "required": ["name", "email", "password", "department_code", "employee_id"],
        "optional": ["designation", "phone"],
        "aliases": {
            "name": ["name", "faculty_name"],
            "email": ["email"],
            "password": ["password", "initial_password"],
            "department_code": ["department_code", "dept_code"],
            "employee_id": ["employee_id", "faculty_id", "emp_id"],
            "designation": ["designation"],
            "phone": ["phone", "mobile"],
        },
    },
    "students": {
        "required": [
            "roll_number",
            "name",
            "password",
            "department_code",
            "program_code",
            "batch_code",
            "class_code",
            "section_code",
            "current_academic_year",
            "current_semester_number",
        ],
        "optional": ["admission_date"],
        "aliases": {
            "roll_number": ["roll_number", "roll_no"],
            "name": ["name", "student_name"],
            "password": ["password", "initial_password"],
            "department_code": ["department_code", "dept_code"],
            "program_code": ["program_code"],
            "batch_code": ["batch_code"],
            "class_code": ["class_code"],
            "section_code": ["section_code"],
            "current_academic_year": ["current_academic_year", "academic_year"],
            "current_semester_number": [
                "current_semester_number",
                "semester_number",
            ],
            "admission_date": ["admission_date"],
        },
    },
    "parents": {
        "required": ["name", "email", "password"],
        "optional": ["phone", "student_roll_number", "relationship_type"],
        "aliases": {
            "name": ["name", "parent_name"],
            "email": ["email"],
            "password": ["password", "initial_password"],
            "phone": ["phone", "mobile"],
            "student_roll_number": ["student_roll_number", "roll_number"],
            "relationship_type": ["relationship_type", "relationship"],
        },
    },
    "enrollments": {
        "required": [
            "student_roll_number",
            "course_code",
            "academic_year_name",
            "semester_number",
        ],
        "optional": [],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number", "sem_number"],
        },
    },
    "faculty_courses": {
        "required": [
            "employee_id",
            "course_code",
            "academic_year_name",
            "semester_number",
        ],
        "optional": ["section_code", "class_code", "batch_code"],
        "aliases": {
            "employee_id": ["employee_id", "faculty_id"],
            "course_code": ["course_code"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number", "sem_number"],
            "section_code": ["section_code"],
            "class_code": ["class_code"],
            "batch_code": ["batch_code"],
        },
    },
}

OPERATIONAL_IMPORT_TYPES: dict[str, ImportTypeConfig] = {
    "attendance": {
        "required": [
            "student_roll_number",
            "course_code",
            "academic_year_name",
            "semester_number",
            "attendance_date",
            "status",
        ],
        "optional": [],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number", "roll_no"],
            "course_code": ["course_code", "course"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number", "sem_number"],
            "attendance_date": ["attendance_date", "date"],
            "status": ["status", "attendance_status"],
        },
    },
    "ca_marks": {
        "required": [
            "student_roll_number",
            "course_code",
            "academic_year_name",
            "semester_number",
            "obtained_marks",
        ],
        "optional": [
            "assessment_type",
            "assessment_name",
            "assessment_date",
            "max_marks",
        ],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number", "sem_number"],
            "assessment_type": ["assessment_type", "type"],
            "assessment_name": ["assessment_name", "assessment"],
            "assessment_date": ["assessment_date", "date"],
            "max_marks": ["max_marks", "maximum_marks"],
            "obtained_marks": ["obtained_marks", "marks_obtained", "marks", "score"],
        },
    },
    "mid_term_marks": {
        "required": [
            "student_roll_number",
            "course_code",
            "academic_year_name",
            "semester_number",
            "obtained_marks",
        ],
        "optional": [
            "assessment_type",
            "assessment_name",
            "assessment_date",
            "max_marks",
        ],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number", "sem_num"],
            "assessment_type": ["assessment_type"],
            "assessment_name": ["assessment_name"],
            "assessment_date": ["assessment_date", "exam_date"],
            "max_marks": ["max_marks"],
            "obtained_marks": ["obtained_marks", "marks_obtained"],
        },
    },
    "end_sem_marks": {
        "required": [
            "student_roll_number",
            "course_code",
            "academic_year_name",
            "semester_number",
            "obtained_marks",
        ],
        "optional": ["exam_date", "max_marks", "assessment_name"],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number"],
            "exam_date": ["exam_date", "assessment_date"],
            "max_marks": ["max_marks"],
            "obtained_marks": ["obtained_marks", "marks_obtained", "end_marks"],
        },
    },
    "semester_results": {
        "required": [
            "student_roll_number",
            "academic_year_name",
            "semester_number",
        ],
        "optional": ["course_code", "grade", "result_status", "sgpa", "cgpa"],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "academic_year_name": ["academic_year_name", "academic_year"],
            "semester_number": ["semester_number"],
            "course_code": ["course_code", "course"],
            "grade": ["grade"],
            "result_status": ["result_status", "status"],
            "sgpa": ["sgpa"],
            "cgpa": ["cgpa"],
        },
    },
    "backlogs": {
        "required": [
            "student_roll_number",
            "course_code",
            "original_academic_year",
            "original_semester_number",
            "status",
        ],
        "optional": ["attempt_number"],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "original_academic_year": [
                "original_academic_year",
                "academic_year",
                "academic_year_name",
            ],
            "original_semester_number": [
                "original_semester_number",
                "semester_number",
                "original_semester",
            ],
            "status": ["status", "backlog_status"],
            "attempt_number": ["attempt_number", "attempt"],
        },
    },
    "backlog_clearance": {
        "required": [
            "student_roll_number",
            "course_code",
            "original_academic_year",
            "original_semester_number",
            "status",
        ],
        "optional": [
            "clearance_academic_year",
            "clearance_semester_number",
            "clearance_date",
            "grade",
            "end_marks",
        ],
        "aliases": {
            "student_roll_number": ["student_roll_number", "roll_number"],
            "course_code": ["course_code"],
            "original_academic_year": ["original_academic_year", "academic_year"],
            "original_semester_number": [
                "original_semester_number",
                "semester_number",
            ],
            "clearance_academic_year": ["clearance_academic_year"],
            "clearance_semester_number": ["clearance_semester_number"],
            "clearance_date": ["clearance_date"],
            "status": ["status", "clearance_status"],
            "grade": ["grade"],
            "end_marks": ["end_marks", "obtained_marks"],
        },
    },
}

IMPORT_TYPES: dict[str, ImportTypeConfig] = {
    **MASTER_IMPORT_TYPES,
    **OPERATIONAL_IMPORT_TYPES,
}

AVAILABLE_MASTER_IMPORT_COUNT = len(MASTER_IMPORT_TYPES)
AVAILABLE_OPERATIONAL_IMPORT_COUNT = len(OPERATIONAL_IMPORT_TYPES)
COMING_SOON_IMPORT_COUNT = 0

TEMPLATE_EXAMPLE_ROWS: dict[str, dict[str, str]] = {
    "attendance": {
        "student_roll_number": "24CSE001",
        "course_code": "CS301",
        "academic_year_name": "2026-27",
        "semester_number": "5",
        "attendance_date": "2026-10-07",
        "status": "present",
    },
    "ca_marks": {
        "student_roll_number": "24CSE001",
        "course_code": "CS301",
        "academic_year_name": "2026-27",
        "semester_number": "5",
        "assessment_name": "CA-1",
        "max_marks": "30",
        "obtained_marks": "24",
    },
    "mid_term_marks": {
        "student_roll_number": "24CSE001",
        "course_code": "CS301",
        "academic_year_name": "2026-27",
        "semester_number": "5",
        "obtained_marks": "68",
        "max_marks": "100",
    },
    "end_sem_marks": {
        "student_roll_number": "24CSE001",
        "course_code": "CS301",
        "academic_year_name": "2026-27",
        "semester_number": "5",
        "obtained_marks": "72",
        "max_marks": "100",
    },
    "semester_results": {
        "student_roll_number": "24CSE001",
        "academic_year_name": "2026-27",
        "semester_number": "5",
        "course_code": "CS301",
        "grade": "A",
        "result_status": "PASS",
    },
    "backlogs": {
        "student_roll_number": "24CSE001",
        "course_code": "MA201",
        "original_academic_year": "2025-26",
        "original_semester_number": "2",
        "status": "NOT_CLEARED",
    },
    "backlog_clearance": {
        "student_roll_number": "24CSE001",
        "course_code": "MA201",
        "original_academic_year": "2025-26",
        "original_semester_number": "2",
        "status": "CLEARED",
        "grade": "B",
    },
}


def is_operational_import(import_type: str) -> bool:
    return import_type in OPERATIONAL_IMPORT_TYPES


is_operational = is_operational_import


def canonical_fields(import_type: str) -> list[str]:
    cfg = IMPORT_TYPES.get(import_type)
    if not cfg:
        return []
    return [*cfg["required"], *cfg["optional"]]


def suggest_column_mapping(import_type: str, headers: list[str]) -> dict[str, str]:
    cfg = IMPORT_TYPES.get(import_type)
    if not cfg:
        return {}
    normalized = {h: _norm(h) for h in headers}
    mapping: dict[str, str] = {}
    used_targets: set[str] = set()
    for target, alias_list in cfg["aliases"].items():
        for alias in alias_list:
            for header, norm in normalized.items():
                if norm == _norm(alias) and target not in used_targets:
                    mapping[header] = target
                    used_targets.add(target)
                    break
            if target in used_targets:
                break
    return mapping


def _norm(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")
