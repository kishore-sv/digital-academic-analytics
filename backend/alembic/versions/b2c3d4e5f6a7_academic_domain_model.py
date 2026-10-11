"""Academic domain model: batches, class groups, sections, program courses.

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
"""

from __future__ import annotations

import json
import math
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sqlalchemy as sa
from alembic import op

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None

REPORT_PATH = (
    Path(__file__).resolve().parents[2] / "migration_reports" / "academic_domain_migration.json"
)


def _year_number_from_semester(num: int) -> int:
    return max(1, math.ceil(num / 2))


def _parse_section_code(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    if "-" in raw:
        return raw.rsplit("-", 1)[-1]
    return raw


def _normalize_course_type(value: str | None, code: str | None, name: str | None) -> tuple[str, bool]:
    v = (value or "THEORY").upper()
    if v == "LAB":
        return "LAB", False
    if v in ("THEORY",):
        return "THEORY", False
    text = f"{code or ''} {name or ''}".upper()
    if "LAB" in v or text.endswith(" LAB") or (code or "").upper().endswith("L"):
        return "LAB", True
    return "THEORY", True


def _write_report(report: dict[str, Any]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report["generated_at"] = datetime.now(UTC).isoformat()
    REPORT_PATH.write_text(json.dumps(report, indent=2, default=str))


def upgrade() -> None:
    report: dict[str, Any] = {
        "unmapped_students": [],
        "course_type_mappings": [],
        "faculty_course_section_unmapped": [],
        "students_missing_program": [],
    }

    # --- New tables ---
    op.create_table(
        "batches",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("program_id", sa.UUID(), nullable=False),
        sa.Column("admission_year", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.ForeignKeyConstraint(["program_id"], ["programs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "institution_id", "program_id", "admission_year", name="uq_batches_institution_program_year"
        ),
    )
    op.create_index("ix_batches_institution_id", "batches", ["institution_id"])

    op.create_table(
        "class_groups",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("batch_id", sa.UUID(), nullable=False),
        sa.Column("year_number", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("batch_id", "year_number", name="uq_class_groups_batch_year"),
    )
    op.create_index("ix_class_groups_institution_id", "class_groups", ["institution_id"])

    op.create_table(
        "sections",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("class_group_id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["class_group_id"], ["class_groups.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_group_id", "code", name="uq_sections_class_group_code"),
    )
    op.create_index("ix_sections_institution_id", "sections", ["institution_id"])

    op.create_table(
        "program_courses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("program_id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("semester_number", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.ForeignKeyConstraint(["program_id"], ["programs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "program_id", "course_id", "semester_number", name="uq_program_courses_program_course_semester"
        ),
    )
    op.create_index("ix_program_courses_institution_id", "program_courses", ["institution_id"])

    # --- Extend semesters ---
    op.add_column("semesters", sa.Column("year_number", sa.Integer(), nullable=True))

    # --- Extend faculty ---
    op.add_column("faculty", sa.Column("employee_id", sa.String(50), nullable=True))
    op.add_column("faculty", sa.Column("designation", sa.String(100), nullable=True))
    op.add_column("faculty", sa.Column("phone", sa.String(30), nullable=True))

    # --- Extend parents ---
    op.add_column("parents", sa.Column("phone", sa.String(30), nullable=True))

    # --- Extend parent_students ---
    op.add_column(
        "parent_students",
        sa.Column("relationship_type", sa.String(30), nullable=False, server_default="GUARDIAN"),
    )
    op.add_column(
        "parent_students",
        sa.Column("is_primary_guardian", sa.Boolean(), nullable=False, server_default="false"),
    )

    # --- Extend enrollments ---
    op.add_column("enrollments", sa.Column("section_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        "fk_enrollments_section_id", "enrollments", "sections", ["section_id"], ["id"]
    )

    # --- Extend students (new FKs, nullable during backfill) ---
    op.add_column("students", sa.Column("batch_id", sa.UUID(), nullable=True))
    op.add_column("students", sa.Column("class_group_id", sa.UUID(), nullable=True))
    op.add_column("students", sa.Column("section_id", sa.UUID(), nullable=True))
    op.add_column("students", sa.Column("current_semester_id", sa.UUID(), nullable=True))
    op.add_column("students", sa.Column("admission_date", sa.Date(), nullable=True))

    # --- Faculty courses: section_id ---
    op.add_column("faculty_courses", sa.Column("section_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        "fk_faculty_courses_section_id", "faculty_courses", "sections", ["section_id"], ["id"]
    )

    conn = op.get_bind()

    # Backfill semester year_number
    semesters = conn.execute(
        sa.text("SELECT id, number FROM semesters")
    ).mappings().all()
    for sem in semesters:
        yn = _year_number_from_semester(sem["number"])
        conn.execute(
            sa.text("UPDATE semesters SET year_number = :yn WHERE id = :id"),
            {"yn": yn, "id": sem["id"]},
        )

    # Normalize course types
    courses = conn.execute(
        sa.text("SELECT id, course_type, code, name FROM courses")
    ).mappings().all()
    for course in courses:
        new_type, changed = _normalize_course_type(
            course["course_type"], course["code"], course["name"]
        )
        if changed:
            report["course_type_mappings"].append(
                {"course_id": str(course["id"]), "from": course["course_type"], "to": new_type}
            )
        conn.execute(
            sa.text("UPDATE courses SET course_type = :t WHERE id = :id"),
            {"t": new_type, "id": course["id"]},
        )

    # Backfill faculty employee_id
    faculty_rows = conn.execute(
        sa.text("SELECT id FROM faculty WHERE employee_id IS NULL")
    ).mappings().all()
    for idx, row in enumerate(faculty_rows, start=1):
        conn.execute(
            sa.text("UPDATE faculty SET employee_id = :eid WHERE id = :id"),
            {"eid": f"FAC{idx:05d}", "id": row["id"]},
        )

    institutions = conn.execute(sa.text("SELECT id FROM institutions")).mappings().all()

    batch_by_program_year: dict[tuple, uuid.UUID] = {}
    class_group_by_batch_year: dict[tuple, uuid.UUID] = {}
    section_by_class_code: dict[tuple, uuid.UUID] = {}
    semester_by_inst_number: dict[tuple, list] = {}

    for inst in institutions:
        inst_id = inst["id"]
        # Index semesters per institution
        sem_rows = conn.execute(
            sa.text(
                """
                SELECT s.id, s.number, s.year_number, ay.is_current, ay.name, ay.created_at
                FROM semesters s
                JOIN academic_years ay ON ay.id = s.academic_year_id
                WHERE s.institution_id = :iid
                ORDER BY ay.is_current DESC, ay.name DESC, s.number
                """
            ),
            {"iid": inst_id},
        ).mappings().all()
        for sr in sem_rows:
            key = (inst_id, sr["number"])
            semester_by_inst_number.setdefault(key, []).append(sr)

        programs = conn.execute(
            sa.text(
                "SELECT id, code, name, department_id FROM programs WHERE institution_id = :iid"
            ),
            {"iid": inst_id},
        ).mappings().all()
        program_by_dept = {p["department_id"]: p for p in programs}
        default_program = programs[0] if programs else None

        students = conn.execute(
            sa.text(
                """
                SELECT id, department_id, program_id, semester, branch, section, roll_number
                FROM students WHERE institution_id = :iid
                """
            ),
            {"iid": inst_id},
        ).mappings().all()

        for student in students:
            program_id = student["program_id"]
            if not program_id:
                dept_prog = program_by_dept.get(student["department_id"])
                if dept_prog:
                    program_id = dept_prog["id"]
                elif default_program:
                    program_id = default_program["id"]
                if program_id:
                    conn.execute(
                        sa.text("UPDATE students SET program_id = :pid WHERE id = :id"),
                        {"pid": program_id, "id": student["id"]},
                    )
            if not program_id:
                report["students_missing_program"].append(str(student["id"]))
                continue

            sem_num = student["semester"] or 1
            year_num = _year_number_from_semester(sem_num)
            admission_year = 2024 - (year_num - 1)

            batch_key = (inst_id, program_id, admission_year)
            if batch_key not in batch_by_program_year:
                prog = next((p for p in programs if p["id"] == program_id), None)
                prog_code = prog["code"] if prog else "PROG"
                batch_id = uuid.uuid4()
                batch_by_program_year[batch_key] = batch_id
                conn.execute(
                    sa.text(
                        """
                        INSERT INTO batches (id, institution_id, program_id, admission_year, code, name, is_active, created_at, updated_at)
                        VALUES (:id, :iid, :pid, :ay, :code, :name, true, now(), now())
                        """
                    ),
                    {
                        "id": batch_id,
                        "iid": inst_id,
                        "pid": program_id,
                        "ay": admission_year,
                        "code": str(admission_year),
                        "name": f"{prog_code} {admission_year} Batch",
                    },
                )

            batch_id = batch_by_program_year[batch_key]
            cg_key = (batch_id, year_num)
            if cg_key not in class_group_by_batch_year:
                prog = next((p for p in programs if p["id"] == program_id), None)
                prog_code = prog["code"] if prog else "PROG"
                cg_id = uuid.uuid4()
                class_group_by_batch_year[cg_key] = cg_id
                conn.execute(
                    sa.text(
                        """
                        INSERT INTO class_groups (id, institution_id, batch_id, year_number, code, name, created_at, updated_at)
                        VALUES (:id, :iid, :bid, :yn, :code, :name, now(), now())
                        """
                    ),
                    {
                        "id": cg_id,
                        "iid": inst_id,
                        "bid": batch_id,
                        "yn": year_num,
                        "code": f"{prog_code}-{admission_year}-Y{year_num}",
                        "name": f"{prog_code} {admission_year} Batch - {year_num}{'st' if year_num==1 else 'nd' if year_num==2 else 'rd' if year_num==3 else 'th'} Year",
                    },
                )

            class_group_id = class_group_by_batch_year[cg_key]
            section_code = _parse_section_code(student["section"]) or "A"
            sec_key = (class_group_id, section_code)
            if sec_key not in section_by_class_code:
                sec_id = uuid.uuid4()
                section_by_class_code[sec_key] = sec_id
                conn.execute(
                    sa.text(
                        """
                        INSERT INTO sections (id, institution_id, class_group_id, code, name, is_active, created_at, updated_at)
                        VALUES (:id, :iid, :cgid, :code, :name, true, now(), now())
                        """
                    ),
                    {
                        "id": sec_id,
                        "iid": inst_id,
                        "cgid": class_group_id,
                        "code": section_code,
                        "name": f"Section {section_code}",
                    },
                )
            section_id = section_by_class_code[sec_key]

            # Resolve current_semester_id
            candidates = semester_by_inst_number.get((inst_id, sem_num), [])
            current_sem_id = candidates[0]["id"] if candidates else None
            if not current_sem_id and sem_rows:
                current_sem_id = sem_rows[0]["id"]

            if not current_sem_id:
                report["unmapped_students"].append(
                    {"student_id": str(student["id"]), "reason": "no_semester_match", "semester": sem_num}
                )
                continue

            conn.execute(
                sa.text(
                    """
                    UPDATE students SET
                        batch_id = :bid,
                        class_group_id = :cgid,
                        section_id = :sid,
                        current_semester_id = :csid,
                        program_id = :pid
                    WHERE id = :id
                    """
                ),
                {
                    "bid": batch_id,
                    "cgid": class_group_id,
                    "sid": section_id,
                    "csid": current_sem_id,
                    "pid": program_id,
                    "id": student["id"],
                },
            )

    # Faculty course section backfill
    fc_rows = conn.execute(
        sa.text("SELECT id, section, institution_id FROM faculty_courses WHERE section IS NOT NULL")
    ).mappings().all()
    for fc in fc_rows:
        code = _parse_section_code(fc["section"])
        if not code:
            continue
        match = conn.execute(
            sa.text(
                """
                SELECT s.id FROM sections s
                WHERE s.institution_id = :iid AND s.code = :code
                LIMIT 1
                """
            ),
            {"iid": fc["institution_id"], "code": code},
        ).first()
        if match:
            conn.execute(
                sa.text("UPDATE faculty_courses SET section_id = :sid WHERE id = :id"),
                {"sid": match[0], "id": fc["id"]},
            )
        else:
            report["faculty_course_section_unmapped"].append(
                {"faculty_course_id": str(fc["id"]), "section": fc["section"]}
            )

    # Enrollment section from student
    conn.execute(
        sa.text(
            """
            UPDATE enrollments e
            SET section_id = s.section_id
            FROM students s
            WHERE e.student_id = s.id AND e.section_id IS NULL AND s.section_id IS NOT NULL
            """
        )
    )

    _write_report(report)

    # NOT NULL constraints
    op.alter_column("semesters", "year_number", nullable=False)
    op.alter_column("faculty", "employee_id", nullable=False)
    op.create_unique_constraint(
        "uq_faculty_institution_employee_id", "faculty", ["institution_id", "employee_id"]
    )

    # Drop old faculty_courses unique before structural changes
    op.drop_constraint("uq_faculty_course_semester", "faculty_courses", type_="unique")
    op.drop_column("faculty_courses", "section")

    op.alter_column("students", "program_id", nullable=False)
    op.alter_column("students", "batch_id", nullable=False)
    op.alter_column("students", "class_group_id", nullable=False)
    op.alter_column("students", "section_id", nullable=False)
    op.alter_column("students", "current_semester_id", nullable=False)

    op.create_foreign_key("fk_students_batch_id", "students", "batches", ["batch_id"], ["id"])
    op.create_foreign_key(
        "fk_students_class_group_id", "students", "class_groups", ["class_group_id"], ["id"]
    )
    op.create_foreign_key("fk_students_section_id", "students", "sections", ["section_id"], ["id"])
    op.create_foreign_key(
        "fk_students_current_semester_id", "students", "semesters", ["current_semester_id"], ["id"]
    )

    op.drop_column("students", "semester")
    op.drop_column("students", "branch")
    op.drop_column("students", "section")

    op.create_unique_constraint(
        "uq_semesters_institution_year_number",
        "semesters",
        ["institution_id", "academic_year_id", "number"],
    )


def downgrade() -> None:
    op.add_column("students", sa.Column("semester", sa.Integer(), nullable=True))
    op.add_column("students", sa.Column("branch", sa.String(50), nullable=True))
    op.add_column("students", sa.Column("section", sa.String(50), nullable=True))

    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            UPDATE students s
            SET semester = sem.number,
                branch = COALESCE(d.code, 'CSE'),
                section = sec.code
            FROM semesters sem
            LEFT JOIN departments d ON d.id = s.department_id
            LEFT JOIN sections sec ON sec.id = s.section_id
            WHERE s.current_semester_id = sem.id
            """
        )
    )
    op.alter_column("students", "semester", nullable=False, server_default="1")
    op.alter_column("students", "branch", nullable=False, server_default="CSE")

    op.drop_constraint("fk_students_current_semester_id", "students", type_="foreignkey")
    op.drop_constraint("fk_students_section_id", "students", type_="foreignkey")
    op.drop_constraint("fk_students_class_group_id", "students", type_="foreignkey")
    op.drop_constraint("fk_students_batch_id", "students", type_="foreignkey")
    op.drop_column("students", "admission_date")
    op.drop_column("students", "current_semester_id")
    op.drop_column("students", "section_id")
    op.drop_column("students", "class_group_id")
    op.drop_column("students", "batch_id")

    op.add_column("faculty_courses", sa.Column("section", sa.String(50), nullable=True))
    op.drop_constraint("fk_faculty_courses_section_id", "faculty_courses", type_="foreignkey")
    op.drop_column("faculty_courses", "section_id")
    op.create_unique_constraint(
        "uq_faculty_course_semester", "faculty_courses", ["faculty_id", "course_id", "semester_id"]
    )

    op.drop_constraint("fk_enrollments_section_id", "enrollments", type_="foreignkey")
    op.drop_column("enrollments", "section_id")

    op.drop_column("parent_students", "is_primary_guardian")
    op.drop_column("parent_students", "relationship_type")

    op.drop_column("parents", "phone")
    op.drop_constraint("uq_faculty_institution_employee_id", "faculty", type_="unique")
    op.drop_column("faculty", "phone")
    op.drop_column("faculty", "designation")
    op.drop_column("faculty", "employee_id")

    op.drop_constraint("uq_semesters_institution_year_number", "semesters", type_="unique")
    op.drop_column("semesters", "year_number")

    op.drop_index("ix_program_courses_institution_id", "program_courses")
    op.drop_table("program_courses")
    op.drop_index("ix_sections_institution_id", "sections")
    op.drop_table("sections")
    op.drop_index("ix_class_groups_institution_id", "class_groups")
    op.drop_table("class_groups")
    op.drop_index("ix_batches_institution_id", "batches")
    op.drop_table("batches")
