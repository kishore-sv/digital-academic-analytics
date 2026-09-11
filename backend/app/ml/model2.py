"""Model 2 — Pass/fail prediction (HistGradientBoostingClassifier)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from app.ml.model_loader import model_loader

MODEL2_FEATURES = [
    "CA_mark",
    "MID_mark",
    "attendance_percentage",
    "study_hours_per_week",
    "assignment_completion_pct",
    "previous_sgpa",
    "previous_cgpa",
    "backlog_count",
    "course_credits",
    "branch",
    "semester",
]

# Training labels: 0 = FAIL, 1 = PASS
_LABEL_MAP = {0: "FAIL", 1: "PASS"}


def predict_pass_fail(features: dict[str, Any]) -> dict[str, Any]:
    """Predict pass/fail outcome with probabilities."""
    if not model_loader.is_loaded:
        raise RuntimeError("ML models not loaded")

    row = {f: features.get(f) for f in MODEL2_FEATURES}
    df = pd.DataFrame([row])
    model = model_loader.pass_fail_model

    pred_class = int(model.predict(df)[0])
    proba = model.predict_proba(df)[0]

    classes = list(model.classes_)
    fail_idx = classes.index(0) if 0 in classes else 0
    pass_idx = classes.index(1) if 1 in classes else 1

    fail_prob = round(float(proba[fail_idx]), 4)
    pass_prob = round(float(proba[pass_idx]), 4)

    return {
        "prediction": _LABEL_MAP.get(pred_class, "FAIL"),
        "pass_probability": pass_prob,
        "fail_probability": fail_prob,
    }
