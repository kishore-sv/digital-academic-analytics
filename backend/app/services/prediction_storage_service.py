"""Persist ML prediction results from academic data."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.prediction import PredictionResult
from app.models.student import Student
from app.services.feature_preparation import build_features_from_student
from app.services.prediction_service import predict_all


def store_student_prediction(
    db: Session,
    student_id: uuid.UUID,
    institution_id: uuid.UUID,
    semester_id: uuid.UUID | None = None,
) -> PredictionResult:
    """Build features from DB, run all models, and persist the prediction result."""
    features = build_features_from_student(db, student_id, institution_id)
    result = predict_all(features, student_id=str(student_id))

    risk = result["risk"]
    prediction = PredictionResult(
        institution_id=institution_id,
        student_id=student_id,
        semester_id=semester_id,
        predicted_end_marks=result["performance"]["predicted_end_marks"],
        pass_fail_prediction=result["pass_fail"]["prediction"],
        pass_probability=result["pass_fail"]["pass_probability"],
        fail_probability=result["pass_fail"]["fail_probability"],
        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"],
        risk_factors=risk["risk_factors"],
        recommendations=risk["recommendations"],
        input_features=features,
    )
    db.add(prediction)
    return prediction


def seed_predictions_for_institution(
    db: Session,
    institution_id: uuid.UUID,
    replace_existing: bool = False,
) -> int:
    """Generate and store predictions for every student in an institution."""
    if replace_existing:
        db.query(PredictionResult).filter(
            PredictionResult.institution_id == institution_id
        ).delete()

    students = (
        db.query(Student)
        .filter(Student.institution_id == institution_id)
        .all()
    )
    count = 0
    for student in students:
        if not replace_existing:
            existing = (
                db.query(PredictionResult)
                .filter(
                    PredictionResult.student_id == student.id,
                    PredictionResult.institution_id == institution_id,
                )
                .first()
            )
            if existing:
                continue

        from app.models.enrollment import Enrollment

        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student.id,
                Enrollment.institution_id == institution_id,
            )
            .order_by(Enrollment.created_at.desc())
            .first()
        )
        semester_id = enrollment.semester_id if enrollment else None
        store_student_prediction(db, student.id, institution_id, semester_id)
        count += 1
    return count
