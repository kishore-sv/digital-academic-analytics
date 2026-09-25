"""ML demo helpers: metrics, datasets, risk breakdown."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from app.core.config import settings
from app.ml.model_loader import model_loader
from app.ml.risk_engine import _score_feature

from app.ml_demo.constants import (
    ALGORITHM_COMPARISONS,
    DATASET_MODEL_NOTES,
    METRICS_FILES,
    SHARED_DATASET_SEARCH_ORDER,
    SHARED_TRAINING_DATASET_FILENAME,
    UNIVERSITY_DATA_DIRNAME,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]

DATASET_PAGE_SIZE = 20


def models_available() -> bool:
    return model_loader.is_loaded


def get_algorithm_comparison(model_key: str) -> dict[str, Any] | None:
    """Return comparison table + rationale for a demo model tab."""
    base = ALGORITHM_COMPARISONS.get(model_key)
    if not base:
        return None

    comparison = dict(base)
    loaded = load_metrics(model_key)
    if not loaded:
        return comparison

    selected_name = (
        loaded.get("selected_algorithm")
        or loaded.get("model_name")
        or loaded.get("model_type")
    )
    candidates: list[dict[str, Any]] = []
    for row in comparison.get("candidates", []):
        entry = dict(row)
        if selected_name and entry.get("algorithm") == selected_name:
            entry["selected"] = True
        candidates.append(entry)
    comparison["candidates"] = candidates

    # Sync deployed model metrics into the selected row when JSON metrics are present.
    if model_key == "model1" and loaded.get("metrics"):
        m = loaded["metrics"]
        for entry in candidates:
            if entry.get("selected"):
                entry["metrics"] = {
                    "MAE": round(float(m["MAE"]), 3),
                    "RMSE": round(float(m["RMSE"]), 3),
                    "R2": round(float(m["R2"]), 3),
                }
    elif model_key == "model2":
        for entry in candidates:
            if entry.get("selected"):
                entry["metrics"] = {
                    "Accuracy": round(float(loaded["accuracy"]), 4),
                    "FAIL precision": round(float(loaded["fail_precision"]), 4),
                    "FAIL recall": round(float(loaded["fail_recall"]), 4),
                    "FAIL F1": round(float(loaded["fail_f1"]), 4),
                    "ROC-AUC": round(float(loaded["roc_auc"]), 4),
                }
    elif model_key == "model3" and loaded.get("metrics"):
        m = loaded["metrics"]
        for entry in candidates:
            if entry.get("selected"):
                entry["metrics"] = {
                    "Accuracy": round(float(m["accuracy"]), 4),
                    "Macro F1": round(float(m["macro_f1"]), 4),
                    "High-risk F1": round(float(m["high_risk_f1"]), 4),
                }

    if loaded.get("why_chosen"):
        comparison["why_chosen"] = loaded["why_chosen"]
    if loaded.get("why_useful"):
        comparison["why_useful"] = loaded["why_useful"]
    if loaded.get("selected_reason") and model_key == "model2":
        comparison["why_chosen"] = loaded["selected_reason"]

    return comparison


def load_metrics(model_key: str) -> dict[str, Any] | None:
    filename = METRICS_FILES.get(model_key)
    if not filename:
        return None
    path = Path(settings.ML_MODELS_DIR) / filename
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _dataset_search_dirs() -> list[Path]:
    return [
        _REPO_ROOT / UNIVERSITY_DATA_DIRNAME,
        Path(settings.ML_MODELS_DIR),
        _REPO_ROOT / "ml" / "models",
        _REPO_ROOT / "ml" / "data" / "processed",
        _REPO_ROOT / "ml" / "data" / "raw",
    ]


def find_shared_dataset_path() -> Path | None:
    """Resolve the single shared training dataset (same source for Models 1–3)."""
    for filename in SHARED_DATASET_SEARCH_ORDER:
        for base in _dataset_search_dirs():
            path = base / filename
            if path.is_file():
                return path
    return None


@lru_cache(maxsize=8)
def _dataset_shape_cached(path_str: str) -> tuple[int, int]:
    path = Path(path_str)
    # Count lines minus header for large CSVs without loading full file
    with open(path, encoding="utf-8", errors="replace") as f:
        row_count = sum(1 for _ in f) - 1
    header = pd.read_csv(path, nrows=0)
    return row_count, len(header.columns)


def get_dataset_page(model_key: str, page: int) -> dict[str, Any]:
    path = find_shared_dataset_path()
    model_note = DATASET_MODEL_NOTES.get(model_key, "")
    if not path:
        return {
            "available": False,
            "message": "Shared training dataset not found in the current repository.",
            "expected_file": SHARED_TRAINING_DATASET_FILENAME,
            "search_order": list(SHARED_DATASET_SEARCH_ORDER),
            "model_note": model_note,
            "hint": (
                f"Place or generate data under {UNIVERSITY_DATA_DIRNAME}/ at the repo root "
                f"(OUTPUT_DIR in student_results_dataset_and_models_training.py)."
            ),
            "dataset_dir": UNIVERSITY_DATA_DIRNAME,
        }

    page = max(1, page)
    skip = (page - 1) * DATASET_PAGE_SIZE
    path_str = str(path.resolve())
    rows, cols = _dataset_shape_cached(path_str)
    total_pages = max(1, (rows + DATASET_PAGE_SIZE - 1) // DATASET_PAGE_SIZE)

    if skip == 0:
        df = pd.read_csv(path, nrows=DATASET_PAGE_SIZE)
    else:
        df = pd.read_csv(path, skiprows=range(1, skip + 1), nrows=DATASET_PAGE_SIZE)
    numeric_summary: dict[str, dict[str, float]] = {}
    if page == 1:
        sample = pd.read_csv(path, nrows=5000)
        for col in sample.select_dtypes(include="number").columns:
            series = sample[col].dropna()
            if len(series):
                numeric_summary[col] = {
                    "count": int(series.count()),
                    "mean": round(float(series.mean()), 4),
                    "min": round(float(series.min()), 4),
                    "max": round(float(series.max()), 4),
                }

    try:
        path_display = str(path.relative_to(_REPO_ROOT))
    except ValueError:
        path_display = path.name

    return {
        "available": True,
        "filename": path.name,
        "path_display": path_display,
        "shared": True,
        "model_note": model_note,
        "rows": rows,
        "columns": cols,
        "column_names": list(df.columns),
        "page": page,
        "total_pages": total_pages,
        "page_size": DATASET_PAGE_SIZE,
        "records": df.to_dict(orient="records"),
        "numeric_summary": numeric_summary,
    }


def read_training_code(model_key: str) -> dict[str, Any]:
    from app.ml_demo.constants import TRAINING_CODE_PATHS

    paths = TRAINING_CODE_PATHS.get(model_key) or []
    files: list[dict[str, str]] = []
    for path in paths:
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            files.append({"name": path.name, "relative": str(path.relative_to(_REPO_ROOT)), "content": text})
    if not files:
        if model_key == "model3":
            return {
                "available": False,
                "message": "Risk engine source not found in the repository.",
            }
        return {
            "available": False,
            "message": "Training code is not available in the current repository.",
        }
    return {"available": True, "files": files}


def risk_contributions(features: dict[str, Any]) -> list[dict[str, Any]]:
    """Weighted per-feature contributions using the same helpers as risk_engine."""
    if not model_loader.is_loaded:
        return []
    config = model_loader.risk_config
    weights = config["feature_weights"]
    rules = config["scoring_rules"]
    rows: list[dict[str, Any]] = []
    for feature, weight in weights.items():
        value = features.get(feature)
        sub_score = _score_feature(value, rules.get(feature, {}))
        weighted = round(sub_score * weight * 100, 2)
        rows.append(
            {
                "feature": feature,
                "sub_score": round(sub_score, 4),
                "weight": weight,
                "weighted_contribution": weighted,
            }
        )
    return rows
