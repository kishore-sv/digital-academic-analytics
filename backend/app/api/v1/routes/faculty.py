"""Faculty CRUD and student assignment routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.security import hash_password
from app.models.department import Department
from app.models.faculty import Faculty
from app.models.parent import FacultyStudent
from app.models.student import Student
from app.models.user import User
from app.schemas.academic import FacultyCreate, FacultyResponse, FacultyUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/faculty", tags=["faculty"])


def _to_response(faculty: Faculty) -> FacultyResponse:
    return FacultyResponse(
        id=str(faculty.id),
        name=faculty.name,
        email=faculty.user.email if faculty.user else None,
        department_id=str(faculty.department_id),
        user_id=str(faculty.user_id),
    )


@router.get("", response_model=PaginatedResponse[FacultyResponse])
def list_faculty(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(Faculty)
        .options(joinedload(Faculty.user))
        .filter(Faculty.institution_id == current.institution_id)
        .order_by(Faculty.created_at.desc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, lambda f: _to_response(f))


@router.post("", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
def create_faculty(body: FacultyCreate, current: AdminUser, db: DbSession):
    dept_id = parse_uuid(body.department_id, "department_id")
    get_entity_or_404(db, Department, dept_id, current.institution_id)

    existing = (
        db.query(User)
        .filter(
            User.institution_id == current.institution_id,
            User.email == body.email,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        institution_id=current.institution_id,
        email=body.email,
        password_hash=hash_password(body.password),
        role="faculty",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()

    faculty = Faculty(
        institution_id=current.institution_id,
        user_id=user.id,
        name=body.name,
        department_id=dept_id,
    )
    db.add(faculty)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    db.refresh(faculty, ["user"])
    return _to_response(faculty)


@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(faculty_id: str, current: AdminOrFacultyUser, db: DbSession):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    db.refresh(faculty, ["user"])
    return _to_response(faculty)


@router.patch("/{faculty_id}", response_model=FacultyResponse)
def update_faculty(
    faculty_id: str,
    body: FacultyUpdate,
    current: AdminUser,
    db: DbSession,
):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    if body.name is not None:
        faculty.name = body.name
    if body.department_id is not None:
        dept_id = parse_uuid(body.department_id, "department_id")
        get_entity_or_404(db, Department, dept_id, current.institution_id)
        faculty.department_id = dept_id
    db.commit()
    db.refresh(faculty, ["user"])
    return _to_response(faculty)


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: str, current: AdminUser, db: DbSession):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    user = faculty.user
    db.delete(faculty)
    if user:
        db.delete(user)
    db.commit()


@router.get("/{faculty_id}/students", response_model=list[str])
def list_assigned_students(faculty_id: str, current: AdminOrFacultyUser, db: DbSession):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    links = (
        db.query(FacultyStudent)
        .filter(FacultyStudent.faculty_id == faculty.id)
        .all()
    )
    return [str(link.student_id) for link in links]


@router.post(
    "/{faculty_id}/students/{student_id}",
    status_code=status.HTTP_201_CREATED,
)
def assign_student(
    faculty_id: str,
    student_id: str,
    current: AdminUser,
    db: DbSession,
):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    student = get_entity_or_404(
        db, Student, parse_uuid(student_id), current.institution_id
    )
    existing = (
        db.query(FacultyStudent)
        .filter(
            FacultyStudent.faculty_id == faculty.id,
            FacultyStudent.student_id == student.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already assigned")
    db.add(FacultyStudent(faculty_id=faculty.id, student_id=student.id))
    db.commit()
    return {"faculty_id": str(faculty.id), "student_id": str(student.id)}


@router.delete(
    "/{faculty_id}/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unassign_student(
    faculty_id: str,
    student_id: str,
    current: AdminUser,
    db: DbSession,
):
    faculty = get_entity_or_404(
        db, Faculty, parse_uuid(faculty_id), current.institution_id
    )
    student_uuid = parse_uuid(student_id)
    link = (
        db.query(FacultyStudent)
        .filter(
            FacultyStudent.faculty_id == faculty.id,
            FacultyStudent.student_id == student_uuid,
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    db.delete(link)
    db.commit()
