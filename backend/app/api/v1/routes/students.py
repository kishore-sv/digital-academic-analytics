"""Student API routes."""

from uuid import UUID

from app.api.deps import AdminOrFacultyUser, AdminUser, CurrentUserDep, DbSession, StudentUser
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.security import hash_password
from app.models.department import Department
from app.models.program import Program
from app.models.student import Student
from app.models.user import User
from app.schemas.academic import StudentCreate, StudentResponse, StudentUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.authorization_service import assert_student_access, filter_students_query
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/students", tags=["students"])


def _to_response(student: Student) -> StudentResponse:
    return StudentResponse(
        id=str(student.id),
        roll_number=student.roll_number,
        name=student.name,
        department_id=str(student.department_id),
        program_id=str(student.program_id) if student.program_id else None,
        semester=student.semester,
        branch=student.branch,
        section=student.section,
    )


@router.get("", response_model=PaginatedResponse[StudentResponse])
def list_students(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = filter_students_query(db, current.user).order_by(Student.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(body: StudentCreate, current: AdminUser, db: DbSession):
    dept_id = parse_uuid(body.department_id, "department_id")
    get_entity_or_404(db, Department, dept_id, current.institution_id)

    program_id = None
    if body.program_id:
        program_id = parse_uuid(body.program_id, "program_id")
        get_entity_or_404(db, Program, program_id, current.institution_id)

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
        semester=body.semester,
        branch=body.branch,
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
    return _to_response(student)


@router.get("/me", response_model=StudentResponse)
def get_my_student_profile(current: StudentUser, db: DbSession):
    student = (
        db.query(Student)
        .filter(
            Student.user_id == current.id,
            Student.institution_id == current.institution_id,
        )
        .first()
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return _to_response(student)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, current: CurrentUserDep, db: DbSession):
    student = assert_student_access(db, current.user, UUID(student_id))
    return _to_response(student)


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
    if body.name is not None:
        student.name = body.name
    if body.department_id is not None:
        dept_id = parse_uuid(body.department_id, "department_id")
        get_entity_or_404(db, Department, dept_id, current.institution_id)
        student.department_id = dept_id
    if body.program_id is not None:
        program_id = parse_uuid(body.program_id, "program_id")
        get_entity_or_404(db, Program, program_id, current.institution_id)
        student.program_id = program_id
    if body.semester is not None:
        student.semester = body.semester
    if body.branch is not None:
        student.branch = body.branch
    db.commit()
    db.refresh(student)
    return _to_response(student)


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
