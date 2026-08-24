"""Model 2 — Student Pass/Fail Prediction (classification)."""

from typing import Any

import joblib

from src.common.paths import MODEL_2_PATH
from src.model_2.preprocessing import to_feature_dataframe

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_2_PATH)
    return _model


def predict_pass_fail(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Predict PASS/FAIL from 32 UCI input features.

    Returns:
        {
            "prediction": "PASS" | "FAIL",
            "pass_probability": float,
            "fail_probability": float,
        }
    """
    features = to_feature_dataframe(input_data)
    model = _load_model()

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    classes = list(model.named_steps["model"].classes_)

    proba_map = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
    return {
        "prediction": str(prediction),
        "pass_probability": proba_map.get("PASS", 0.0),
        "fail_probability": proba_map.get("FAIL", 0.0),
    }
