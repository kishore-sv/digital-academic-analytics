"""Department CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.department import Department
from app.schemas.academic import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/departments", tags=["departments"])


def _to_response(dept: Department) -> DepartmentResponse:
    return DepartmentResponse(
        id=str(dept.id),
        name=dept.name,
        code=dept.code,
        description=dept.description,
    )


@router.get("", response_model=PaginatedResponse[DepartmentResponse])
def list_departments(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(Department)
        .filter(Department.institution_id == current.institution_id)
        .order_by(Department.name.asc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(body: DepartmentCreate, current: AdminUser, db: DbSession):
    dept = Department(
        institution_id=current.institution_id,
        name=body.name,
        code=body.code,
        description=body.description,
    )
    db.add(dept)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department code already exists")
    db.refresh(dept)
    return _to_response(dept)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: str, current: AdminOrFacultyUser, db: DbSession):
    dept = get_entity_or_404(
        db, Department, parse_uuid(department_id), current.institution_id
    )
    return _to_response(dept)


@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: str,
    body: DepartmentUpdate,
    current: AdminUser,
    db: DbSession,
):
    dept = get_entity_or_404(
        db, Department, parse_uuid(department_id), current.institution_id
    )
    if body.name is not None:
        dept.name = body.name
    if body.code is not None:
        dept.code = body.code
    if body.description is not None:
        dept.description = body.description
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department code already exists")
    db.refresh(dept)
    return _to_response(dept)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: str, current: AdminUser, db: DbSession):
    dept = get_entity_or_404(
        db, Department, parse_uuid(department_id), current.institution_id
    )
    db.delete(dept)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete department with linked programs or users",
        )
