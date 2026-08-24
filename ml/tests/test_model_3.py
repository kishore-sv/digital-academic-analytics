"""Tests for Model 3 — rule-based risk engine."""

import pytest

from src.common.validation import ValidationError
from src.model_3.risk_engine import assess_student_risk


def _valid_input() -> dict:
    return {
        "absences": 6,
        "G1": 10,
        "G2": 9,
        "failures": 1,
        "studytime": 2,
    }


def test_assess_student_risk_valid_output():
    result = assess_student_risk(_valid_input())
    assert 0 <= result["risk_score"] <= 100
    assert result["risk_level"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["risk_indicators"], list)
    assert "component_risks" in result


def test_assess_student_risk_invalid_input_raises():
    with pytest.raises(ValidationError):
        assess_student_risk({"absences": 6, "G1": 10})


def test_g3_does_not_affect_risk_score():
    base = _valid_input()
    with_g3 = {**base, "G3": 20}
    assert assess_student_risk(base)["risk_score"] == assess_student_risk(with_g3)[
        "risk_score"
    ]


def test_risk_levels_respect_thresholds():
    low = assess_student_risk(
        {"absences": 2, "G1": 14, "G2": 15, "failures": 0, "studytime": 4}
    )
    assert low["risk_level"] == "LOW"

    high = assess_student_risk(
        {"absences": 20, "G1": 8, "G2": 5, "failures": 3, "studytime": 1}
    )
    assert high["risk_level"] == "HIGH"
