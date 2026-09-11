"""Authorization and access-scope helpers."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.tenant import get_tenant_entity
from app.models.faculty import Faculty
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.student import Student
from app.models.user import User


def _get_faculty_profile(db: Session, user: User) -> Faculty | None:
    return (
        db.query(Faculty)
        .filter(Faculty.user_id == user.id, Faculty.institution_id == user.institution_id)
        .first()
    )


def _get_parent_profile(db: Session, user: User) -> Parent | None:
    return (
        db.query(Parent)
        .filter(Parent.user_id == user.id, Parent.institution_id == user.institution_id)
        .first()
    )


def get_assigned_student_ids(db: Session, faculty_id: uuid.UUID) -> list[uuid.UUID]:
    rows = (
        db.query(FacultyStudent.student_id)
        .filter(FacultyStudent.faculty_id == faculty_id)
        .all()
    )
    return [row[0] for row in rows]


def get_linked_child_ids(db: Session, parent_id: uuid.UUID) -> list[uuid.UUID]:
    rows = (
        db.query(ParentStudent.student_id)
        .filter(ParentStudent.parent_id == parent_id)
        .all()
    )
    return [row[0] for row in rows]


def get_accessible_student_ids(db: Session, user: User) -> list[uuid.UUID] | None:
    """
    Return accessible student IDs for the user.
    None means all students in the institution (institution_admin).
    """
    if user.role == "institution_admin":
        return None

    if user.role == "faculty":
        faculty = _get_faculty_profile(db, user)
        if not faculty:
            return []
        return get_assigned_student_ids(db, faculty.id)

    if user.role == "parent":
        parent = _get_parent_profile(db, user)
        if not parent:
            return []
        return get_linked_child_ids(db, parent.id)

    if user.role == "student":
        student = (
            db.query(Student)
            .filter(Student.user_id == user.id, Student.institution_id == user.institution_id)
            .first()
        )
        return [student.id] if student else []

    return []


def can_access_student(db: Session, user: User, student_id: uuid.UUID) -> bool:
    student = get_tenant_entity(db, Student, student_id, user.institution_id)
    if not student:
        return False

    accessible = get_accessible_student_ids(db, user)
    if accessible is None:
        return True
    return student_id in accessible


def assert_student_access(db: Session, user: User, student_id: uuid.UUID) -> Student:
    student = get_tenant_entity(db, Student, student_id, user.institution_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    if not can_access_student(db, user, student_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return student


def assert_enrollment_access(db: Session, user: User, enrollment_id: uuid.UUID):
    from app.models.enrollment import Enrollment

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.id == enrollment_id,
            Enrollment.institution_id == user.institution_id,
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    assert_student_access(db, user, enrollment.student_id)
    return enrollment


def filter_students_query(db: Session, user: User):
    """Return a Student query scoped to the user's accessible students."""
    query = db.query(Student).filter(Student.institution_id == user.institution_id)
    accessible = get_accessible_student_ids(db, user)
    if accessible is None:
        return query
    if not accessible:
        return query.filter(Student.id == None)  # noqa: E711 — empty result set
    return query.filter(Student.id.in_(accessible))
