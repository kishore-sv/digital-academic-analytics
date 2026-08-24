"""Path helpers for ML module."""

from pathlib import Path

ML_ROOT = Path(__file__).resolve().parents[2]

MODEL_1_PATH = ML_ROOT / "models" / "model_1" / "performance_model.pkl"
MODEL_2_PATH = ML_ROOT / "models" / "model_2" / "pass_fail_model.pkl"
MODEL_3_CONFIG_PATH = ML_ROOT / "models" / "model_3" / "risk_engine_config.json"
DATA_RAW_PATH = ML_ROOT / "data" / "raw" / "student-mat.csv"
