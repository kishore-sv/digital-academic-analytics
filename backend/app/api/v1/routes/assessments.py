"""Assessment and assessment mark CRUD routes."""

from app.api.deps import AdminOrFacultyUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.course import Course
from app.models.enrollment import Assessment, AssessmentMark, Enrollment
from app.schemas.academic import (
    AssessmentCreate,
    AssessmentMarkCreate,
    AssessmentMarkResponse,
    AssessmentMarkUpdate,
    AssessmentResponse,
    AssessmentUpdate,
    BulkMarksGridRequest,
    BulkMarksRequest,
    MarksGridResponse,
    MarksRosterResponse,
    RosterStudentRow,
)
from app.services.marks_entry_service import build_marks_grid
from app.services.result_calculation_service import recalculate_after_marks_save
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.authorization_service import assert_enrollment_access
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/assessments", tags=["assessments"])


def _to_assessment_response(assessment: Assessment) -> AssessmentResponse:
    return AssessmentResponse(
        id=str(assessment.id),
        course_id=str(assessment.course_id),
        name=assessment.name,
        assessment_type=assessment.assessment_type,
        max_marks=assessment.max_marks,
        date=assessment.date,
    )


def _to_mark_response(mark: AssessmentMark) -> AssessmentMarkResponse:
    return AssessmentMarkResponse(
        id=str(mark.id),
        enrollment_id=str(mark.enrollment_id),
        assessment_id=str(mark.assessment_id),
        marks_obtained=mark.marks_obtained,
    )


@router.get("/marks", response_model=PaginatedResponse[AssessmentMarkResponse])
def list_marks(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    assessment_id: str | None = None,
    enrollment_id: str | None = None,
):
    query = db.query(AssessmentMark).filter(
        AssessmentMark.institution_id == current.institution_id
    )
    if assessment_id:
        query = query.filter(
            AssessmentMark.assessment_id == parse_uuid(assessment_id, "assessment_id")
        )
    if enrollment_id:
        query = query.filter(
            AssessmentMark.enrollment_id == parse_uuid(enrollment_id, "enrollment_id")
        )
    query = query.order_by(AssessmentMark.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_mark_response)


@router.post("/marks", response_model=AssessmentMarkResponse, status_code=status.HTTP_201_CREATED)
def create_mark(body: AssessmentMarkCreate, current: AdminOrFacultyUser, db: DbSession):
    enrollment_id = parse_uuid(body.enrollment_id, "enrollment_id")
    assessment_id = parse_uuid(body.assessment_id, "assessment_id")
    assert_enrollment_access(db, current.user, enrollment_id)
    get_entity_or_404(db, Assessment, assessment_id, current.institution_id)
    mark = AssessmentMark(
        institution_id=current.institution_id,
        enrollment_id=enrollment_id,
        assessment_id=assessment_id,
        marks_obtained=body.marks_obtained,
    )
    db.add(mark)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mark already exists for this enrollment and assessment",
        )
    db.refresh(mark)
    return _to_mark_response(mark)


@router.patch("/marks/{mark_id}", response_model=AssessmentMarkResponse)
def update_mark(
    mark_id: str,
    body: AssessmentMarkUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    mark = get_entity_or_404(
        db, AssessmentMark, parse_uuid(mark_id), current.institution_id
    )
    assert_enrollment_access(db, current.user, mark.enrollment_id)
    mark.marks_obtained = body.marks_obtained
    db.commit()
    db.refresh(mark)
    return _to_mark_response(mark)


@router.delete("/marks/{mark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mark(mark_id: str, current: AdminOrFacultyUser, db: DbSession):
    mark = get_entity_or_404(
        db, AssessmentMark, parse_uuid(mark_id), current.institution_id
    )
    assert_enrollment_access(db, current.user, mark.enrollment_id)
    db.delete(mark)
    db.commit()


@router.get("", response_model=PaginatedResponse[AssessmentResponse])
def list_assessments(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    course_id: str | None = None,
):
    query = db.query(Assessment).filter(
        Assessment.institution_id == current.institution_id
    )
    if course_id:
        query = query.filter(Assessment.course_id == parse_uuid(course_id, "course_id"))
    query = query.order_by(Assessment.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_assessment_response)


@router.post("", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(body: AssessmentCreate, current: AdminOrFacultyUser, db: DbSession):
    course_id = parse_uuid(body.course_id, "course_id")
    get_entity_or_404(db, Course, course_id, current.institution_id)
    assessment = Assessment(
        institution_id=current.institution_id,
        course_id=course_id,
        name=body.name,
        assessment_type=body.assessment_type,
        max_marks=body.max_marks,
        date=body.date,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return _to_assessment_response(assessment)


@router.get("/marks-grid", response_model=MarksGridResponse)
def get_marks_grid(
    current: AdminOrFacultyUser,
    db: DbSession,
    course_id: str = Query(...),
    semester_id: str | None = Query(None),
    department_id: str | None = Query(None),
    program_id: str | None = Query(None),
    section: str | None = Query(None),
    search: str | None = Query(None),
):
    from app.services.authorization_service import get_accessible_student_ids

    course_uuid = parse_uuid(course_id, "course_id")
    get_entity_or_404(db, Course, course_uuid, current.institution_id)
    accessible = get_accessible_student_ids(db, current.user)

    grid = build_marks_grid(
        db,
        current.institution_id,
        course_uuid,
        semester_id=parse_uuid(semester_id, "semester_id") if semester_id else None,
        department_id=parse_uuid(department_id, "department_id") if department_id else None,
        program_id=parse_uuid(program_id, "program_id") if program_id else None,
        section=section,
        search=search,
        accessible_student_ids=accessible,
    )
    if not grid.get("course_id"):
        raise HTTPException(status_code=404, detail="Course not found")
    return MarksGridResponse(**grid)


@router.get("/roster", response_model=MarksRosterResponse)
def get_marks_roster(
    current: AdminOrFacultyUser,
    db: DbSession,
    course_id: str = Query(...),
    assessment_id: str = Query(...),
    semester_id: str | None = Query(None),
):
    course_uuid = parse_uuid(course_id, "course_id")
    assessment_uuid = parse_uuid(assessment_id, "assessment_id")
    assessment = get_entity_or_404(db, Assessment, assessment_uuid, current.institution_id)
    if assessment.course_id != course_uuid:
        raise HTTPException(status_code=400, detail="Assessment does not belong to course")

    query = db.query(Enrollment).filter(
        Enrollment.institution_id == current.institution_id,
        Enrollment.course_id == course_uuid,
    )
    if semester_id:
        query = query.filter(
            Enrollment.semester_id == parse_uuid(semester_id, "semester_id")
        )
    enrollments = query.all()

    from app.services.authorization_service import get_accessible_student_ids

    accessible = get_accessible_student_ids(db, current.user)
    rows = []
    for enrollment in enrollments:
        if accessible is not None and enrollment.student_id not in accessible:
            continue
        student = enrollment.student
        mark = (
            db.query(AssessmentMark)
            .filter(
                AssessmentMark.enrollment_id == enrollment.id,
                AssessmentMark.assessment_id == assessment_uuid,
            )
            .first()
        )
        cr = enrollment.course_result
        rows.append(
            RosterStudentRow(
                enrollment_id=str(enrollment.id),
                student_id=str(student.id),
                student_name=student.name,
                roll_number=student.roll_number,
                attendance_percentage=enrollment.attendance_percentage,
                mark_id=str(mark.id) if mark else None,
                marks_obtained=mark.marks_obtained if mark else None,
                end_marks=cr.end_marks if cr else None,
                course_result_status=cr.status if cr else None,
            )
        )
    return MarksRosterResponse(
        assessment_id=str(assessment.id),
        assessment_name=assessment.name,
        max_marks=assessment.max_marks,
        students=rows,
    )


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(assessment_id: str, current: AdminOrFacultyUser, db: DbSession):
    assessment = get_entity_or_404(
        db, Assessment, parse_uuid(assessment_id), current.institution_id
    )
    return _to_assessment_response(assessment)


@router.patch("/{assessment_id}", response_model=AssessmentResponse)
def update_assessment(
    assessment_id: str,
    body: AssessmentUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    assessment = get_entity_or_404(
        db, Assessment, parse_uuid(assessment_id), current.institution_id
    )
    if body.name is not None:
        assessment.name = body.name
    if body.assessment_type is not None:
        assessment.assessment_type = body.assessment_type
    if body.max_marks is not None:
        assessment.max_marks = body.max_marks
    if body.date is not None:
        assessment.date = body.date
    db.commit()
    db.refresh(assessment)
    return _to_assessment_response(assessment)


def _process_bulk_marks(
    db: DbSession,
    current: AdminOrFacultyUser,
    entries: list,
    *,
    allow_null: bool = False,
    recalculate_results: bool = True,
    trigger_predictions: bool = False,
) -> list[AssessmentMark]:
    results: list[AssessmentMark] = []
    affected_enrollment_ids: set = set()
    for entry in entries:
        enrollment_id = parse_uuid(entry.enrollment_id, "enrollment_id")
        assessment_id = parse_uuid(entry.assessment_id, "assessment_id")
        assert_enrollment_access(db, current.user, enrollment_id)
        assessment = get_entity_or_404(
            db, Assessment, assessment_id, current.institution_id
        )
        marks_value = entry.marks_obtained
        if marks_value is None:
            if not allow_null:
                continue
            existing = (
                db.query(AssessmentMark)
                .filter(
                    AssessmentMark.enrollment_id == enrollment_id,
                    AssessmentMark.assessment_id == assessment_id,
                    AssessmentMark.institution_id == current.institution_id,
                )
                .first()
            )
            if existing:
                db.delete(existing)
            continue
        if marks_value < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Marks cannot be negative",
            )
        if marks_value > assessment.max_marks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Marks exceed max_marks ({assessment.max_marks}) for {assessment.name}",
            )
        existing = (
            db.query(AssessmentMark)
            .filter(
                AssessmentMark.enrollment_id == enrollment_id,
                AssessmentMark.assessment_id == assessment_id,
                AssessmentMark.institution_id == current.institution_id,
            )
            .first()
        )
        if existing:
            existing.marks_obtained = marks_value
            mark = existing
        else:
            mark = AssessmentMark(
                institution_id=current.institution_id,
                enrollment_id=enrollment_id,
                assessment_id=assessment_id,
                marks_obtained=marks_value,
            )
            db.add(mark)
        results.append(mark)
        affected_enrollment_ids.add(enrollment_id)

    if recalculate_results and affected_enrollment_ids:
        recalculate_after_marks_save(
            db, list(affected_enrollment_ids), current.institution_id
        )

    db.commit()
    for mark in results:
        db.refresh(mark)

    if trigger_predictions and affected_enrollment_ids:
        from app.services.prediction_storage_service import store_student_prediction
        from app.models.enrollment import Enrollment

        student_ids: set = set()
        for eid in affected_enrollment_ids:
            enr = db.query(Enrollment).filter(Enrollment.id == eid).first()
            if enr:
                student_ids.add(enr.student_id)
        for sid in student_ids:
            try:
                store_student_prediction(db, sid, current.institution_id)
            except Exception:
                pass

    return results


@router.post("/marks/bulk", response_model=list[AssessmentMarkResponse])
def bulk_upsert_marks(
    body: BulkMarksRequest,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    results = _process_bulk_marks(db, current, body.entries, recalculate_results=True)
    return [_to_mark_response(m) for m in results]


@router.post("/marks/bulk-grid", response_model=list[AssessmentMarkResponse])
def bulk_upsert_marks_grid(
    body: BulkMarksGridRequest,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    results = _process_bulk_marks(
        db,
        current,
        body.entries,
        allow_null=True,
        recalculate_results=body.recalculate_results,
        trigger_predictions=body.trigger_predictions,
    )
    return [_to_mark_response(m) for m in results]


@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(assessment_id: str, current: AdminOrFacultyUser, db: DbSession):
    assessment = get_entity_or_404(
        db, Assessment, parse_uuid(assessment_id), current.institution_id
    )
    db.delete(assessment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete assessment with linked marks",
        )
