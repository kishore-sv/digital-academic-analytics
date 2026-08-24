"""Model 3 — Rule-based Student At-Risk Detection."""

import json
from pathlib import Path
from typing import Any

from src.common.paths import MODEL_3_CONFIG_PATH
from src.common.validation import validate_risk_input

_config: dict[str, Any] | None = None


def _load_config(config_path: Path | None = None) -> dict[str, Any]:
    global _config
    if _config is None:
        path = config_path or MODEL_3_CONFIG_PATH
        with open(path, encoding="utf-8") as f:
            _config = json.load(f)
    return _config


def _component_level(value: int, low: int, medium: int, high_min: int | None = None) -> int:
    """Map numeric input to component risk: 0=LOW, 1=MEDIUM, 2=HIGH."""
    if high_min is not None:
        if value >= high_min:
            return 2
        if value == medium:
            return 1
        return 0
    if value <= low:
        return 0
    if value <= medium:
        return 1
    return 2


def calculate_risk(
    absences: int,
    g1: float,
    g2: float,
    failures: int,
    studytime: int,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Calculate weighted risk score and level from JSON configuration."""
    cfg = config or _load_config()
    weights = cfg["weights"]
    thresholds = cfg["thresholds"]

    absence_t = thresholds["absence"]
    absence_risk = _component_level(
        absences, absence_t["low_max"], absence_t["medium_max"]
    )

    perf_t = thresholds["performance"]
    if g2 >= perf_t["low_min"]:
        performance_risk = 0
    elif g2 >= perf_t["medium_min"]:
        performance_risk = 1
    else:
        performance_risk = 2

    performance_trend = g2 - g1
    if performance_trend > 0:
        trend_risk = 0
    elif performance_trend == 0:
        trend_risk = 1
    else:
        trend_risk = 2

    fail_t = thresholds["failures"]
    failure_risk = _component_level(
        failures, fail_t["low"], fail_t["medium"], fail_t["high_min"]
    )

    study_t = thresholds["studytime"]
    if studytime >= study_t["low_min"]:
        studytime_risk = 0
    elif studytime == study_t["medium"]:
        studytime_risk = 1
    else:
        studytime_risk = 2

    risk_score = (
        (absence_risk / 2) * weights["absence"]
        + (performance_risk / 2) * weights["performance"]
        + (trend_risk / 2) * weights["trend"]
        + (failure_risk / 2) * weights["failure"]
        + (studytime_risk / 2) * weights["studytime"]
    )

    level_t = thresholds["risk_level"]
    if risk_score <= level_t["low_max"]:
        risk_level = "LOW"
    elif risk_score <= level_t["medium_max"]:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "absence_risk": absence_risk,
        "performance_risk": performance_risk,
        "trend_risk": trend_risk,
        "failure_risk": failure_risk,
        "studytime_risk": studytime_risk,
    }


def get_risk_indicators(
    absences: int,
    g1: float,
    g2: float,
    failures: int,
    studytime: int,
    config: dict[str, Any] | None = None,
) -> list[str]:
    """Return actionable risk indicators based on configured thresholds."""
    cfg = config or _load_config()
    thresholds = cfg["thresholds"]
    indicators: list[str] = []

    absence_t = thresholds["absence"]
    if absences > absence_t["medium_max"]:
        indicators.append("High Absence")
    elif absences > absence_t["low_max"]:
        indicators.append("Moderate Absence")

    perf_t = thresholds["performance"]
    if g2 < perf_t["medium_min"]:
        indicators.append("Low Current Performance")
    elif g2 < perf_t["low_min"]:
        indicators.append("Moderate Current Performance")

    trend = g2 - g1
    if trend < 0:
        indicators.append("Declining Performance")
    elif trend == 0:
        indicators.append("Stable Performance")

    fail_t = thresholds["failures"]
    if failures >= fail_t["high_min"]:
        indicators.append("Multiple Previous Failures")
    elif failures == fail_t["medium"]:
        indicators.append("Previous Failure")

    study_t = thresholds["studytime"]
    if studytime == study_t["high"]:
        indicators.append("Low Study Time")
    elif studytime == study_t["medium"]:
        indicators.append("Moderate Study Time")

    return indicators


def assess_student_risk(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Full risk assessment for a student.

    Input: absences, G1, G2, failures, studytime (G3 is ignored if present).

    Returns:
        risk_score, risk_level, risk_indicators, and component risk values.
    """
    validate_risk_input(input_data)

    absences = int(input_data["absences"])
    g1 = float(input_data["G1"])
    g2 = float(input_data["G2"])
    failures = int(input_data["failures"])
    studytime = int(input_data["studytime"])

    risk_result = calculate_risk(absences, g1, g2, failures, studytime)
    indicators = get_risk_indicators(absences, g1, g2, failures, studytime)

    return {
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "risk_indicators": indicators,
        "component_risks": {
            "absence_risk": risk_result["absence_risk"],
            "performance_risk": risk_result["performance_risk"],
            "trend_risk": risk_result["trend_risk"],
            "failure_risk": risk_result["failure_risk"],
            "studytime_risk": risk_result["studytime_risk"],
        },
    }
