"""Model 3 — Weighted risk scoring engine (rule-based, config-driven)."""

from __future__ import annotations

from typing import Any

from app.ml.model_loader import model_loader

RISK_FEATURES = [
    "attendance_percentage",
    "previous_cgpa",
    "backlog_count",
    "current_failed_courses",
    "low_performance_course_count",
    "study_hours_per_week",
    "assignment_completion_percentage",
    "performance_trend",
]


def _match_numeric_rule(value: float, rule_key: str) -> bool:
    if rule_key == "missing":
        return False
    if rule_key.endswith("+"):
        return value >= float(rule_key[:-1])
    if rule_key.startswith("<"):
        return value < float(rule_key[1:])
    if "-" in rule_key:
        parts = rule_key.split("-", 1)
        try:
            return float(parts[0]) <= value <= float(parts[1])
        except ValueError:
            return False
    try:
        return value == float(rule_key)
    except ValueError:
        return False


def _score_feature(value: Any, rules: dict[str, float]) -> float:
    """Map a feature value to a risk sub-score using config rules."""
    if value is None:
        return rules.get("missing", 0.0)

    # Categorical (performance_trend)
    if isinstance(value, str) and not value.replace(".", "").replace("-", "").isdigit():
        return rules.get(value.upper(), rules.get(value, 0.0))

    num = float(value)

    # Exact integer match first (backlog_count, current_failed_courses, etc.)
    for rule_key, score in rules.items():
        if rule_key in ("missing",):
            continue
        if rule_key.isdigit() and num == int(rule_key):
            return score

    # Range / threshold rules (order matters — check specific before general)
    for rule_key, score in rules.items():
        if rule_key in ("missing",) or rule_key.isdigit():
            continue
        if _match_numeric_rule(num, rule_key):
            return score

    return 0.0


def _classify_risk_level(score: float, thresholds: dict) -> str:
    if score <= thresholds["LOW"]["max"]:
        return "LOW"
    if score <= thresholds["MEDIUM"]["max"]:
        return "MEDIUM"
    return "HIGH"


def calculate_risk_score(features: dict[str, Any]) -> float:
    """Calculate weighted risk score (0–100) from features."""
    if not model_loader.is_loaded:
        raise RuntimeError("ML models not loaded")

    config = model_loader.risk_config
    weights = config["feature_weights"]
    rules = config["scoring_rules"]

    score = 0.0
    for feature, weight in weights.items():
        value = features.get(feature)
        feature_rules = rules.get(feature, {})
        sub_score = _score_feature(value, feature_rules)
        score += sub_score * weight * 100

    return round(score, 2)


def predict_risk(features: dict[str, Any]) -> dict[str, Any]:
    """Calculate risk score and level from features."""
    config = model_loader.risk_config
    score = calculate_risk_score(features)
    level = _classify_risk_level(score, config["risk_thresholds"])
    return {"risk_score": score, "risk_level": level}
