"""Integration tests — model loading and pipeline inspection."""

import joblib

from src.common.paths import MODEL_1_PATH, MODEL_2_PATH, MODEL_3_CONFIG_PATH
from src.model_3.risk_engine import _load_config


def test_model_1_pipeline_loads():
    pipeline = joblib.load(MODEL_1_PATH)
    assert hasattr(pipeline, "predict")
    assert "model" in pipeline.named_steps


def test_model_2_pipeline_loads():
    pipeline = joblib.load(MODEL_2_PATH)
    assert hasattr(pipeline, "predict")
    assert hasattr(pipeline, "predict_proba")
    classes = list(pipeline.named_steps["model"].classes_)
    assert set(classes) == {"PASS", "FAIL"}


def test_risk_config_loads():
    config = _load_config(MODEL_3_CONFIG_PATH)
    assert "weights" in config
    assert "thresholds" in config
    assert config["weights"]["absence"] == 25
