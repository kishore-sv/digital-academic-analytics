"""Prediction service combining Model 1, Model 2, and Model 3."""

from __future__ import annotations

from typing import Any

from app.ml.model1 import predict_performance
from app.ml.model2 import predict_pass_fail
from app.ml.risk_engine import predict_risk
from app.services.recommendation_service import (
    detect_risk_factors,
    generate_recommendations,
)


def predict_performance_only(features: dict[str, Any]) -> dict[str, Any]:
    predicted = predict_performance(features)
    return {"predicted_end_marks": predicted}


def predict_pass_fail_only(features: dict[str, Any]) -> dict[str, Any]:
    return predict_pass_fail(features)


def predict_risk_only(features: dict[str, Any]) -> dict[str, Any]:
    risk = predict_risk(features)
    risk["risk_factors"] = detect_risk_factors(features)
    risk["recommendations"] = generate_recommendations(features)
    return risk


def predict_all(
    features: dict[str, Any], student_id: str | None = None
) -> dict[str, Any]:
    """Run all three prediction models and return combined result."""
    result: dict[str, Any] = {}
    if student_id:
        result["student_id"] = student_id

    result["performance"] = predict_performance_only(features)
    result["pass_fail"] = predict_pass_fail_only(features)
    result["risk"] = predict_risk_only(features)
    return result
