"""Academic year and semester routes."""

from app.api.deps import AdminOrFacultyUser, DbSession
from app.models.academic_year import AcademicYear
from app.models.semester import Semester
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/academic", tags=["academic"])


class AcademicYearResponse(BaseModel):
    id: str
    name: str
    is_current: bool

    model_config = {"from_attributes": True}


class SemesterResponse(BaseModel):
    id: str
    academic_year_id: str
    number: int
    name: str

    model_config = {"from_attributes": True}


@router.get("/years", response_model=list[AcademicYearResponse])
def list_academic_years(current: AdminOrFacultyUser, db: DbSession):
    years = (
        db.query(AcademicYear)
        .filter(AcademicYear.institution_id == current.institution_id)
        .order_by(AcademicYear.name.desc())
        .all()
    )
    return [
        AcademicYearResponse(
            id=str(y.id),
            name=y.name,
            is_current=y.is_current,
        )
        for y in years
    ]


@router.get("/semesters", response_model=list[SemesterResponse])
def list_semesters(
    current: AdminOrFacultyUser,
    db: DbSession,
    academic_year_id: str | None = None,
):
    query = db.query(Semester).filter(Semester.institution_id == current.institution_id)
    if academic_year_id:
        from app.api.v1.helpers import parse_uuid

        query = query.filter(
            Semester.academic_year_id == parse_uuid(academic_year_id, "academic_year_id")
        )
    semesters = query.order_by(Semester.number).all()
    return [
        SemesterResponse(
            id=str(s.id),
            academic_year_id=str(s.academic_year_id),
            number=s.number,
            name=s.name,
        )
        for s in semesters
    ]
