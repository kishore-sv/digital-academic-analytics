"""Academic year and semester routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.academic_responses import semester_response
from app.api.v1.helpers import get_entity_or_404, parse_uuid
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from app.schemas.academic import (
    AcademicYearCreate,
    AcademicYearResponse,
    AcademicYearUpdate,
    SemesterCreate,
    SemesterResponse,
    SemesterUpdate,
)
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/academic", tags=["academic"])


def _clear_other_current_years(db, institution_id, exclude_id=None):
    query = db.query(AcademicYear).filter(
        AcademicYear.institution_id == institution_id,
        AcademicYear.is_current.is_(True),
    )
    if exclude_id:
        query = query.filter(AcademicYear.id != exclude_id)
    for year in query.all():
        year.is_current = False


@router.get("/years", response_model=list[AcademicYearResponse])
def list_academic_years(current: AdminOrFacultyUser, db: DbSession):
    years = (
        db.query(AcademicYear)
        .filter(AcademicYear.institution_id == current.institution_id)
        .order_by(AcademicYear.name.desc())
        .all()
    )
    return [
        AcademicYearResponse(id=str(y.id), name=y.name, is_current=y.is_current) for y in years
    ]


@router.post("/years", response_model=AcademicYearResponse, status_code=status.HTTP_201_CREATED)
def create_academic_year(body: AcademicYearCreate, current: AdminUser, db: DbSession):
    year = AcademicYear(
        institution_id=current.institution_id,
        name=body.name,
        is_current=body.is_current,
    )
    db.add(year)
    if body.is_current:
        _clear_other_current_years(db, current.institution_id)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Academic year exists")
    db.refresh(year)
    return AcademicYearResponse(id=str(year.id), name=year.name, is_current=year.is_current)


@router.patch("/years/{year_id}", response_model=AcademicYearResponse)
def update_academic_year(
    year_id: str, body: AcademicYearUpdate, current: AdminUser, db: DbSession
):
    year = get_entity_or_404(
        db, AcademicYear, parse_uuid(year_id), current.institution_id
    )
    if body.name is not None:
        year.name = body.name
    if body.is_current is not None:
        year.is_current = body.is_current
        if body.is_current:
            _clear_other_current_years(db, current.institution_id, exclude_id=year.id)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Academic year conflict")
    db.refresh(year)
    return AcademicYearResponse(id=str(year.id), name=year.name, is_current=year.is_current)


@router.delete("/years/{year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_academic_year(year_id: str, current: AdminUser, db: DbSession):
    year = get_entity_or_404(
        db, AcademicYear, parse_uuid(year_id), current.institution_id
    )
    db.delete(year)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete academic year with linked semesters",
        )


@router.get("/semesters", response_model=list[SemesterResponse])
def list_semesters(
    current: AdminOrFacultyUser,
    db: DbSession,
    academic_year_id: str | None = None,
):
    query = db.query(Semester).filter(Semester.institution_id == current.institution_id)
    if academic_year_id:
        query = query.filter(
            Semester.academic_year_id == parse_uuid(academic_year_id, "academic_year_id")
        )
    semesters = query.order_by(Semester.number).all()
    return [semester_response(s) for s in semesters]


@router.post("/semesters", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(body: SemesterCreate, current: AdminUser, db: DbSession):
    ay_id = parse_uuid(body.academic_year_id, "academic_year_id")
    get_entity_or_404(db, AcademicYear, ay_id, current.institution_id)
    semester = Semester(
        institution_id=current.institution_id,
        academic_year_id=ay_id,
        number=body.number,
        name=body.name,
        year_number=body.year_number,
    )
    db.add(semester)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Semester exists")
    db.refresh(semester)
    return semester_response(semester)


@router.patch("/semesters/{semester_id}", response_model=SemesterResponse)
def update_semester(
    semester_id: str, body: SemesterUpdate, current: AdminUser, db: DbSession
):
    semester = get_entity_or_404(
        db, Semester, parse_uuid(semester_id), current.institution_id
    )
    if body.number is not None:
        semester.number = body.number
    if body.name is not None:
        semester.name = body.name
    if body.year_number is not None:
        semester.year_number = body.year_number
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Semester conflict")
    db.refresh(semester)
    return semester_response(semester)


@router.delete("/semesters/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_semester(semester_id: str, current: AdminUser, db: DbSession):
    semester = get_entity_or_404(
        db, Semester, parse_uuid(semester_id), current.institution_id
    )
    db.delete(semester)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete semester with linked enrollments",
        )
