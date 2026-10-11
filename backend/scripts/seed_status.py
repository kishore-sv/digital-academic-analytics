"""Print Demo University seed counts (departments, students, etc.)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.core.seed_data import INSTITUTION_1_NAME
from app.core.seed_validate import (
    FULL_DATASET_DEPARTMENTS,
    FULL_DATASET_STUDENTS,
    FULL_DATASET_BRANCH_CODES,
    STUDENTS_PER_BRANCH,
)
from app.models.department import Department
from app.models.institution import Institution
from app.models.student import Student
from sqlalchemy import func


def main() -> None:
    db = SessionLocal()
    try:
        inst = (
            db.query(Institution)
            .filter(Institution.name == INSTITUTION_1_NAME)
            .first()
        )
        if not inst:
            print("No Demo University institution found. Run: uv run python scripts/reseed.py")
            return

        dept_count = (
            db.query(Department)
            .filter(Department.institution_id == inst.id)
            .count()
        )
        student_count = (
            db.query(Student).filter(Student.institution_id == inst.id).count()
        )
        by_dept = dict(
            db.query(Department.code, func.count(Student.id))
            .join(Student, Student.department_id == Department.id)
            .filter(Student.institution_id == inst.id)
            .group_by(Department.code)
            .all()
        )

        print(f"{INSTITUTION_1_NAME}")
        print(f"  Departments: {dept_count} (expected {FULL_DATASET_DEPARTMENTS})")
        print(f"  Students:    {student_count} (expected {FULL_DATASET_STUDENTS})")
        for code in FULL_DATASET_BRANCH_CODES:
            n = by_dept.get(code, 0)
            mark = "ok" if n == STUDENTS_PER_BRANCH else "MISSING"
            print(f"    {code}: {n} ({mark})")

        if dept_count == FULL_DATASET_DEPARTMENTS and student_count == FULL_DATASET_STUDENTS:
            print("\nFull dataset is loaded.")
        else:
            print(
                "\nDataset is incomplete. Restore the full seed with:\n"
                "  cd backend && uv run python scripts/reseed.py"
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()
