"""Tests for Model 2 — pass/fail prediction."""

import pandas as pd

from src.common.paths import DATA_RAW_PATH
from src.model_2.predictor import predict_pass_fail


def _first_student_row() -> dict:
    df = pd.read_csv(DATA_RAW_PATH, sep=";")
    row = df.iloc[0]
    return row.drop("G3").to_dict()


def test_predict_pass_fail_valid_output():
    result = predict_pass_fail(_first_student_row())
    assert result["prediction"] in {"PASS", "FAIL"}
    assert 0 <= result["pass_probability"] <= 1
    assert 0 <= result["fail_probability"] <= 1
    assert abs(
        result["pass_probability"] + result["fail_probability"] - 1.0
    ) < 1e-6
