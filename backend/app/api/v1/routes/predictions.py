"""Prediction API routes."""

import uuid

from app.api.deps import CurrentUserDep, DbSession, PredictionToolUser
from app.models.prediction import PredictionResult
from app.schemas.prediction import (
    AllPredictionsResponse,
    PassFailFeatures,
    PassFailPredictionResponse,
    PerformanceFeatures,
    PerformancePredictionResponse,
    RiskFeatures,
    RiskPredictionResponse,
    StudentPredictionRequest,
)
from app.services.authorization_service import assert_student_access, get_accessible_student_ids
from app.services.feature_preparation import build_features_from_student
from app.services.prediction_service import (
    predict_pass_fail_only,
    predict_performance_only,
    predict_risk_only,
)
from app.services.prediction_storage_service import (
    seed_predictions_for_institution,
    store_student_prediction,
)
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _as_string_list(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, dict):
        return [str(v) for v in value.values()]
    return [str(value)]


@router.post("/performance", response_model=PerformancePredictionResponse)
def predict_performance_endpoint(
    body: PerformanceFeatures,
    current: PredictionToolUser,
):
    result = predict_performance_only(body.model_dump())
    return PerformancePredictionResponse(**result)


@router.post("/pass-fail", response_model=PassFailPredictionResponse)
def predict_pass_fail_endpoint(
    body: PassFailFeatures,
    current: PredictionToolUser,
):
    result = predict_pass_fail_only(body.model_dump())
    return PassFailPredictionResponse(**result)


@router.post("/risk", response_model=RiskPredictionResponse)
def predict_risk_endpoint(
    body: RiskFeatures,
    current: PredictionToolUser,
):
    result = predict_risk_only(body.model_dump())
    return RiskPredictionResponse(**result)


@router.post("/all", response_model=AllPredictionsResponse)
def predict_all_endpoint(
    body: PerformanceFeatures,
    current: PredictionToolUser,
    student_id: str | None = None,
):
    features = body.model_dump()
    risk_features = {
        "attendance_percentage": features["attendance_percentage"],
        "previous_cgpa": features["previous_cgpa"],
        "backlog_count": features["backlog_count"],
        "current_failed_courses": 0,
        "low_performance_course_count": 0,
        "study_hours_per_week": features["study_hours_per_week"],
        "assignment_completion_percentage": features["assignment_completion_pct"],
        "performance_trend": "STABLE",
    }
    perf = predict_performance_only(features)
    pf = predict_pass_fail_only(features)
    risk = predict_risk_only(risk_features)

    return AllPredictionsResponse(
        student_id=student_id,
        performance=PerformancePredictionResponse(**perf),
        pass_fail=PassFailPredictionResponse(**pf),
        risk=RiskPredictionResponse(**risk),
    )


@router.post("/student", response_model=AllPredictionsResponse)
def predict_for_student(
    body: StudentPredictionRequest,
    current: CurrentUserDep,
    db: DbSession,
):
    assert_student_access(db, current.user, uuid.UUID(body.student_id))

    try:
        build_features_from_student(
            db, uuid.UUID(body.student_id), current.institution_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    from app.models.enrollment import Enrollment

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == uuid.UUID(body.student_id),
            Enrollment.institution_id == current.institution_id,
        )
        .order_by(Enrollment.created_at.desc())
        .first()
    )
    semester_id = enrollment.semester_id if enrollment else None

    prediction = store_student_prediction(
        db,
        uuid.UUID(body.student_id),
        current.institution_id,
        semester_id,
    )
    db.commit()
    db.refresh(prediction)

    return AllPredictionsResponse(
        student_id=body.student_id,
        performance=PerformancePredictionResponse(
            predicted_end_marks=prediction.predicted_end_marks or 0.0
        ),
        pass_fail=PassFailPredictionResponse(
            prediction=prediction.pass_fail_prediction or "PASS",
            pass_probability=prediction.pass_probability or 0.0,
            fail_probability=prediction.fail_probability or 0.0,
        ),
        risk=RiskPredictionResponse(
            risk_score=prediction.risk_score or 0.0,
            risk_level=prediction.risk_level or "LOW",
            risk_factors=_as_string_list(prediction.risk_factors),
            recommendations=_as_string_list(prediction.recommendations),
        ),
    )


class RegenerateResponse(BaseModel):
    regenerated_count: int


@router.post("/regenerate", response_model=RegenerateResponse)
def regenerate_predictions(
    current: CurrentUserDep,
    db: DbSession,
    replace_existing: bool = True,
):
    if current.role not in ("institution_admin", "faculty"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if current.role == "faculty":
        accessible = get_accessible_student_ids(db, current.user)
        if not accessible:
            return RegenerateResponse(regenerated_count=0)
        count = 0
        from app.models.enrollment import Enrollment

        for student_id in accessible:
            enrollment = (
                db.query(Enrollment)
                .filter(
                    Enrollment.student_id == student_id,
                    Enrollment.institution_id == current.institution_id,
                )
                .order_by(Enrollment.created_at.desc())
                .first()
            )
            semester_id = enrollment.semester_id if enrollment else None
            if replace_existing:
                db.query(PredictionResult).filter(
                    PredictionResult.student_id == student_id,
                    PredictionResult.institution_id == current.institution_id,
                ).delete()
            store_student_prediction(
                db, student_id, current.institution_id, semester_id
            )
            count += 1
        db.commit()
        return RegenerateResponse(regenerated_count=count)

    count = seed_predictions_for_institution(
        db, current.institution_id, replace_existing=replace_existing
    )
    db.commit()
    return RegenerateResponse(regenerated_count=count)
