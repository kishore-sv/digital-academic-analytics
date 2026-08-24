"""Model 1 — Student Performance Prediction (regression)."""

from typing import Any

import joblib

from src.common.paths import MODEL_1_PATH
from src.common.validation import ValidationError
from src.model_1.preprocessing import to_feature_dataframe

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_1_PATH)
    return _model


def predict_performance(input_data: dict[str, Any]) -> dict[str, float]:
    """
    Predict final grade (G3) from 32 UCI input features.

    Returns:
        {"predicted_g3": float}
    """
    try:
        features = to_feature_dataframe(input_data)
    except ValidationError:
        raise

    model = _load_model()
    prediction = float(model.predict(features)[0])
    return {"predicted_g3": prediction}
