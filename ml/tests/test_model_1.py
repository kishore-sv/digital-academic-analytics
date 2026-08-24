"""Tests for Model 1 — performance prediction."""

import pandas as pd

from src.common.paths import DATA_RAW_PATH
from src.model_1.predictor import predict_performance


def _first_student_row() -> dict:
    df = pd.read_csv(DATA_RAW_PATH, sep=";")
    row = df.iloc[0]
    return row.drop("G3").to_dict()


def test_predict_performance_returns_numeric_g3():
    result = predict_performance(_first_student_row())
    assert "predicted_g3" in result
    assert isinstance(result["predicted_g3"], float)
    assert 0 <= result["predicted_g3"] <= 20
