"""Student API routes."""

from uuid import UUID

from app.api.deps import AdminOrFacultyUser, AdminUser, CurrentUserDep, DbSession, StudentUser
from app.api.v1.academic_responses import student_response
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.security import hash_password
from app.models.department import Department
from app.models.student import Student
from app.models.user import User
from app.schemas.academic import StudentCreate, StudentResponse, StudentUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.academic_validation_service import validate_student_academic_graph
from app.services.authorization_service import assert_student_access, filter_students_query
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=PaginatedResponse[StudentResponse])
def list_students(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        filter_students_query(db, current.user)
        .options(
            joinedload(Student.current_semester),
            joinedload(Student.section),
            joinedload(Student.batch),
        )
        .order_by(Student.created_at.desc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, student_response)


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(body: StudentCreate, current: AdminUser, db: DbSession):
    dept_id = parse_uuid(body.department_id, "department_id")
    program_id = parse_uuid(body.program_id, "program_id")
    batch_id = parse_uuid(body.batch_id, "batch_id")
    class_group_id = parse_uuid(body.class_group_id, "class_group_id")
    section_id = parse_uuid(body.section_id, "section_id")
    current_semester_id = parse_uuid(body.current_semester_id, "current_semester_id")

    get_entity_or_404(db, Department, dept_id, current.institution_id)
    validate_student_academic_graph(
        db,
        current.institution_id,
        department_id=dept_id,
        program_id=program_id,
        batch_id=batch_id,
        class_group_id=class_group_id,
        section_id=section_id,
        current_semester_id=current_semester_id,
    )

    existing = (
        db.query(Student)
        .filter(
            Student.institution_id == current.institution_id,
            Student.roll_number == body.roll_number,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Roll number already exists"
        )

    user = User(
        institution_id=current.institution_id,
        email=None,
        password_hash=hash_password(body.password),
        role="student",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()

    student = Student(
        institution_id=current.institution_id,
        user_id=user.id,
        roll_number=body.roll_number,
        name=body.name,
        department_id=dept_id,
        program_id=program_id,
        batch_id=batch_id,
        class_group_id=class_group_id,
        section_id=section_id,
        current_semester_id=current_semester_id,
        admission_date=body.admission_date,
    )
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Roll number already exists"
        )
    db.refresh(student)
    db.refresh(student, ["current_semester", "section", "batch"])
    return student_response(student)


@router.get("/me", response_model=StudentResponse)
def get_my_student_profile(current: StudentUser, db: DbSession):
    student = (
        db.query(Student)
        .options(
            joinedload(Student.current_semester),
            joinedload(Student.section),
            joinedload(Student.batch),
        )
        .filter(
            Student.user_id == current.id,
            Student.institution_id == current.institution_id,
        )
        .first()
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student_response(student)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, current: CurrentUserDep, db: DbSession):
    student = assert_student_access(db, current.user, UUID(student_id))
    db.refresh(student, ["current_semester", "section", "batch"])
    return student_response(student)


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: str,
    body: StudentUpdate,
    current: AdminUser,
    db: DbSession,
):
    student = get_entity_or_404(
        db, Student, parse_uuid(student_id), current.institution_id
    )
    dept_id = student.department_id
    program_id = student.program_id
    batch_id = student.batch_id
    class_group_id = student.class_group_id
    section_id = student.section_id
    current_semester_id = student.current_semester_id

    if body.name is not None:
        student.name = body.name
    if body.department_id is not None:
        dept_id = parse_uuid(body.department_id, "department_id")
        get_entity_or_404(db, Department, dept_id, current.institution_id)
        student.department_id = dept_id
    if body.program_id is not None:
        program_id = parse_uuid(body.program_id, "program_id")
        student.program_id = program_id
    if body.batch_id is not None:
        batch_id = parse_uuid(body.batch_id, "batch_id")
        student.batch_id = batch_id
    if body.class_group_id is not None:
        class_group_id = parse_uuid(body.class_group_id, "class_group_id")
        student.class_group_id = class_group_id
    if body.section_id is not None:
        section_id = parse_uuid(body.section_id, "section_id")
        student.section_id = section_id
    if body.current_semester_id is not None:
        current_semester_id = parse_uuid(body.current_semester_id, "current_semester_id")
        student.current_semester_id = current_semester_id
    if body.admission_date is not None:
        student.admission_date = body.admission_date

    validate_student_academic_graph(
        db,
        current.institution_id,
        department_id=dept_id,
        program_id=program_id,
        batch_id=batch_id,
        class_group_id=class_group_id,
        section_id=section_id,
        current_semester_id=current_semester_id,
    )

    db.commit()
    db.refresh(student, ["current_semester", "section", "batch"])
    return student_response(student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, current: AdminUser, db: DbSession):
    student = get_entity_or_404(
        db, Student, parse_uuid(student_id), current.institution_id
    )
    user = student.user
    db.delete(student)
    if user:
        db.delete(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete student with linked academic records",
        )
