"""Centralized ML model loader — loads artifacts once at startup."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib

from app.core.config import settings


class ModelLoader:
    """Loads and holds trained ML artifacts."""

    def __init__(self) -> None:
        self.performance_model: Any = None
        self.pass_fail_model: Any = None
        self.risk_config: dict[str, Any] = {}
        self._loaded = False

    def load(self, models_dir: str | Path | None = None) -> None:
        """Load all ML artifacts. Raises FileNotFoundError if required files missing."""
        base = Path(models_dir or settings.ML_MODELS_DIR)

        model1_path = base / "model1_endterm_histgradientboosting.pkl"
        model2_path = base / "model2_pass_fail_histgradientboosting.pkl"
        risk_config_path = base / "model3_risk_engine_config.json"

        required = [model1_path, model2_path, risk_config_path]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise FileNotFoundError(
                f"Required ML artifacts not found: {', '.join(missing)}"
            )

        self.performance_model = joblib.load(model1_path)
        self.pass_fail_model = joblib.load(model2_path)
        with open(risk_config_path, encoding="utf-8") as f:
            self.risk_config = json.load(f)

        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded


model_loader = ModelLoader()
