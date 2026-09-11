"""Model 1 — End-term performance prediction (HistGradientBoostingRegressor)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.ml.model_loader import model_loader

MODEL1_FEATURES = [
    "CA_mark",
    "MID_mark",
    "attendance_percentage",
    "study_hours_per_week",
    "assignment_completion_pct",
    "previous_sgpa",
    "previous_cgpa",
    "backlog_count",
    "course_credits",
    "course_type",
    "branch",
    "semester",
]


def predict_performance(features: dict[str, Any]) -> float:
    """Predict end-term marks from feature dict. Returns value clamped to 0–100."""
    if not model_loader.is_loaded:
        raise RuntimeError("ML models not loaded")

    row = {f: features.get(f) for f in MODEL1_FEATURES}
    df = pd.DataFrame([row])
    raw = float(model_loader.performance_model.predict(df)[0])
    return round(max(0.0, min(100.0, raw)), 2)
