"""Marks entry roster filtering and grid building."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.enrollment import Assessment, AssessmentMark, Enrollment
from app.models.program import Program
from app.models.semester import Semester
from app.models.student import Student
from app.services.authorization_service import get_accessible_student_ids


def get_assigned_course_ids(db: Session, faculty_id: uuid.UUID) -> list[uuid.UUID]:
    from app.models.faculty_course import FacultyCourse

    rows = (
        db.query(FacultyCourse.course_id)
        .filter(FacultyCourse.faculty_id == faculty_id)
        .all()
    )
    return [r[0] for r in rows]


def filter_enrollments_query(
    db: Session,
    institution_id: uuid.UUID,
    *,
    course_id: uuid.UUID,
    semester_id: uuid.UUID | None = None,
    department_id: uuid.UUID | None = None,
    program_id: uuid.UUID | None = None,
    section: str | None = None,
    search: str | None = None,
    accessible_student_ids: list[uuid.UUID] | None = None,
):
    query = (
        db.query(Enrollment)
        .join(Student, Enrollment.student_id == Student.id)
        .filter(
            Enrollment.institution_id == institution_id,
            Enrollment.course_id == course_id,
        )
        .options(
            joinedload(Enrollment.student),
            joinedload(Enrollment.course_result),
            joinedload(Enrollment.assessment_marks).joinedload(AssessmentMark.assessment),
        )
    )
    if semester_id:
        query = query.filter(Enrollment.semester_id == semester_id)
    if department_id:
        query = query.filter(Student.department_id == department_id)
    if program_id:
        query = query.filter(Student.program_id == program_id)
    if section:
        query = query.filter(Student.section == section)
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Student.name.ilike(pattern)) | (Student.roll_number.ilike(pattern))
        )
    if accessible_student_ids is not None:
        if not accessible_student_ids:
            return query.filter(Enrollment.id == None)  # noqa: E711
        query = query.filter(Enrollment.student_id.in_(accessible_student_ids))
    return query.order_by(Student.roll_number)


def build_marks_grid(
    db: Session,
    institution_id: uuid.UUID,
    course_id: uuid.UUID,
    semester_id: uuid.UUID | None = None,
    department_id: uuid.UUID | None = None,
    program_id: uuid.UUID | None = None,
    section: str | None = None,
    search: str | None = None,
    accessible_student_ids: list[uuid.UUID] | None = None,
) -> dict:
    course = db.query(Course).filter(Course.id == course_id, Course.institution_id == institution_id).first()
    if not course:
        return {"assessments": [], "students": [], "course": None}

    assessments = (
        db.query(Assessment)
        .filter(Assessment.course_id == course_id, Assessment.institution_id == institution_id)
        .order_by(Assessment.assessment_type, Assessment.name)
        .all()
    )

    enrollments = filter_enrollments_query(
        db,
        institution_id,
        course_id=course_id,
        semester_id=semester_id,
        department_id=department_id,
        program_id=program_id,
        section=section,
        search=search,
        accessible_student_ids=accessible_student_ids,
    ).all()

    assessment_cols = [
        {
            "id": str(a.id),
            "name": a.name,
            "assessment_type": a.assessment_type,
            "max_marks": a.max_marks,
        }
        for a in assessments
    ]

    students = []
    for enrollment in enrollments:
        student = enrollment.student
        marks_map = {str(m.assessment_id): m for m in enrollment.assessment_marks}
        mark_cells = []
        for a in assessments:
            m = marks_map.get(str(a.id))
            mark_cells.append({
                "assessment_id": str(a.id),
                "mark_id": str(m.id) if m else None,
                "marks_obtained": m.marks_obtained if m else None,
            })
        cr = enrollment.course_result
        students.append({
            "enrollment_id": str(enrollment.id),
            "student_id": str(student.id),
            "student_name": student.name,
            "roll_number": student.roll_number,
            "section": student.section,
            "attendance_percentage": enrollment.attendance_percentage,
            "marks": mark_cells,
            "total_marks": cr.end_marks if cr else None,
            "grade": cr.grade if cr else None,
            "status": cr.status if cr else None,
        })

    return {
        "course_id": str(course.id),
        "course_name": course.name,
        "course_code": course.code,
        "course_type": course.course_type,
        "assessments": assessment_cols,
        "students": students,
    }
