"""Input validation for ML models."""

from typing import Any

import pandas as pd

from src.common.features import FEATURE_COLUMNS, RISK_INPUT_FIELDS


class ValidationError(ValueError):
    """Raised when model input validation fails."""


def _require_fields(data: dict[str, Any], fields: list[str]) -> None:
    missing = [f for f in fields if f not in data]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")


def validate_uci_features(data: dict[str, Any]) -> None:
    """Validate input for Model 1 and Model 2 (32 UCI features)."""
    _require_fields(data, FEATURE_COLUMNS)


def validate_risk_input(data: dict[str, Any]) -> None:
    """Validate input for Model 3 risk engine."""
    _require_fields(data, RISK_INPUT_FIELDS)

    absences = data["absences"]
    g1 = data["G1"]
    g2 = data["G2"]
    failures = data["failures"]
    studytime = data["studytime"]

    for name, value in [
        ("absences", absences),
        ("G1", g1),
        ("G2", g2),
        ("failures", failures),
        ("studytime", studytime),
    ]:
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{name} must be numeric, got {type(value).__name__}")

    if absences < 0:
        raise ValidationError("absences must be >= 0")
    if not 0 <= g1 <= 20:
        raise ValidationError("G1 must be between 0 and 20")
    if not 0 <= g2 <= 20:
        raise ValidationError("G2 must be between 0 and 20")
    if failures < 0:
        raise ValidationError("failures must be >= 0")
    if studytime not in (1, 2, 3, 4):
        raise ValidationError("studytime must be 1, 2, 3, or 4")


def to_feature_dataframe(data: dict[str, Any]) -> pd.DataFrame:
    """Build a single-row DataFrame with UCI feature columns."""
    validate_uci_features(data)
    return pd.DataFrame([{col: data[col] for col in FEATURE_COLUMNS}])
