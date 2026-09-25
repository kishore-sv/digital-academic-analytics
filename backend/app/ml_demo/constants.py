"""Example inputs and dataset/training file mapping for the ML demo."""

from __future__ import annotations

from pathlib import Path

# Demo presets verified against loaded models (high/low, pass/fail, LOW/HIGH risk).
MODEL1_EXAMPLES: dict[str, dict[str, str | int | float]] = {
    "high": {
        "CA_mark": 42,
        "MID_mark": 44,
        "attendance_percentage": 92,
        "study_hours_per_week": 22,
        "assignment_completion_pct": 95,
        "previous_sgpa": 8.2,
        "previous_cgpa": 8.0,
        "backlog_count": 0,
        "course_credits": 4,
        "course_type": "THEORY",
        "branch": "CSE",
        "semester": 5,
    },
    "low": {
        "CA_mark": 18,
        "MID_mark": 20,
        "attendance_percentage": 52,
        "study_hours_per_week": 6,
        "assignment_completion_pct": 35,
        "previous_sgpa": 5.2,
        "previous_cgpa": 5.0,
        "backlog_count": 3,
        "course_credits": 4,
        "course_type": "THEORY",
        "branch": "CSE",
        "semester": 5,
    },
}

MODEL2_EXAMPLES: dict[str, dict[str, str | int | float]] = {
    "pass": {
        "CA_mark": 42,
        "MID_mark": 44,
        "attendance_percentage": 92,
        "study_hours_per_week": 22,
        "assignment_completion_pct": 95,
        "previous_sgpa": 8.2,
        "previous_cgpa": 8.0,
        "backlog_count": 0,
        "course_credits": 4,
        "branch": "CSE",
        "semester": 5,
    },
    "fail": {
        "CA_mark": 18,
        "MID_mark": 20,
        "attendance_percentage": 52,
        "study_hours_per_week": 6,
        "assignment_completion_pct": 35,
        "previous_sgpa": 5.2,
        "previous_cgpa": 5.0,
        "backlog_count": 3,
        "course_credits": 4,
        "branch": "CSE",
        "semester": 5,
    },
}

MODEL3_EXAMPLES: dict[str, dict[str, str | int | float]] = {
    "low": {
        "attendance_percentage": 90,
        "previous_cgpa": 8.5,
        "backlog_count": 0,
        "current_failed_courses": 0,
        "low_performance_course_count": 0,
        "study_hours_per_week": 25,
        "assignment_completion_percentage": 95,
        "performance_trend": "IMPROVING",
    },
    "high": {
        "attendance_percentage": 50,
        "previous_cgpa": 4.5,
        "backlog_count": 4,
        "current_failed_courses": 3,
        "low_performance_course_count": 4,
        "study_hours_per_week": 5,
        "assignment_completion_percentage": 30,
        "performance_trend": "DECLINING",
    },
}


def resolve_example_form(tab: str, example: str | None) -> dict[str, str | int | float]:
    if not example:
        return {}
    key = example.strip().lower()
    presets: dict[str, dict[str, dict[str, str | int | float]]] = {
        "model1": MODEL1_EXAMPLES,
        "model2": MODEL2_EXAMPLES,
        "model3": MODEL3_EXAMPLES,
    }
    tab_presets = presets.get(tab, {})
    if key in tab_presets:
        return dict(tab_presets[key])
    return {}

# One synthetic dataset run (see student_results_dataset_and_models_training.py).
# Training script OUTPUT_DIR = "university_data" at repository root.
UNIVERSITY_DATA_DIRNAME = "university_data"

SHARED_TRAINING_DATASET_FILENAME = "student_semester_features.csv"

SHARED_DATASET_SEARCH_ORDER: tuple[str, ...] = (
    SHARED_TRAINING_DATASET_FILENAME,
    "model1_regression_dataset.csv",
)

DATASET_MODEL_NOTES: dict[str, str] = {
    "model1": "Model 1 uses TARGET_END_MARKS from exports of this shared synthetic dataset.",
    "model2": "Model 2 uses TARGET_PASS_FAIL from the same synthetic simulation.",
    "model3": "Model 3 risk evaluation uses semester-level features from the same simulation.",
}

METRICS_FILES: dict[str, str] = {
    "model1": "model1_metrics.json",
    "model2": "model2_metrics.json",
    "model3": "model3_metrics.json",
}

TRAINING_CODE_PATHS: dict[str, list[Path]] = {
    "model1": [],
    "model2": [],
    "model3": [],
}

_RISK_ENGINE_REL = Path("backend/app/ml/risk_engine.py")
_TRAINING_SCRIPT_REL = Path("ml/models/student_results_dataset_and_models_training.py")
_RISK_CONFIG_REL = Path("ml/models/model3_risk_engine_config.json")


def resolve_repo_paths(repo_root: Path) -> None:
    """Populate training code paths relative to repository root."""
    training = repo_root / _TRAINING_SCRIPT_REL
    risk_engine = repo_root / _RISK_ENGINE_REL
    risk_config = repo_root / _RISK_CONFIG_REL

    if training.is_file():
        TRAINING_CODE_PATHS["model1"] = [training]
        TRAINING_CODE_PATHS["model2"] = [training]
    if risk_engine.is_file():
        TRAINING_CODE_PATHS["model3"] = [risk_engine]
        if risk_config.is_file():
            TRAINING_CODE_PATHS["model3"].append(risk_config)


_REPO_ROOT = Path(__file__).resolve().parents[3]
resolve_repo_paths(_REPO_ROOT)

# Algorithm comparison shown on the ML demo (metrics from university-scale training).
ALGORITHM_COMPARISONS: dict[str, dict[str, object]] = {
    "model1": {
        "title": "Regression algorithm comparison",
        "metric_labels": ["MAE", "RMSE", "R²"],
        "why_chosen": (
            "HistGradientBoosting achieved the lowest RMSE and highest R² on the held-out "
            "test set while handling mixed numeric and categorical ERP features."
        ),
        "why_useful": (
            "Estimates expected end-term marks so mentors and dashboards can flag students "
            "who may need support before final exams."
        ),
        "candidates": [
            {
                "algorithm": "Linear Regression",
                "selected": False,
                "metrics": {"MAE": 5.806, "RMSE": 7.301, "R2": 0.749},
            },
            {
                "algorithm": "Random Forest Regressor",
                "selected": False,
                "metrics": {"MAE": 5.790, "RMSE": 7.266, "R2": 0.752},
            },
            {
                "algorithm": "HistGradientBoostingRegressor",
                "selected": True,
                "metrics": {"MAE": 5.631, "RMSE": 7.071, "R2": 0.764},
            },
        ],
    },
    "model2": {
        "title": "Classification algorithm comparison",
        "metric_labels": [
            "Accuracy",
            "FAIL precision",
            "FAIL recall",
            "FAIL F1",
            "ROC-AUC",
        ],
        "why_chosen": (
            "HistGradientBoosting delivered the highest FAIL recall and ROC-AUC among the "
            "three candidates, which matters most for early-warning pass/fail alerts."
        ),
        "why_useful": (
            "Flags likely course failures while the term is still in progress so advisors "
            "can schedule remediation before results are finalized."
        ),
        "candidates": [
            {
                "algorithm": "Logistic Regression",
                "selected": False,
                "metrics": {
                    "Accuracy": 0.9278,
                    "FAIL precision": 0.1101,
                    "FAIL recall": 0.9626,
                    "FAIL F1": 0.1976,
                    "ROC-AUC": 0.9756,
                },
            },
            {
                "algorithm": "Random Forest Classifier",
                "selected": False,
                "metrics": {
                    "Accuracy": 0.9394,
                    "FAIL precision": 0.1428,
                    "FAIL recall": 0.9185,
                    "FAIL F1": 0.2481,
                    "ROC-AUC": 0.9879,
                },
            },
            {
                "algorithm": "HistGradientBoostingClassifier",
                "selected": True,
                "metrics": {
                    "Accuracy": 0.9533,
                    "FAIL precision": 0.1614,
                    "FAIL recall": 0.9673,
                    "FAIL F1": 0.2767,
                    "ROC-AUC": 0.9906,
                },
            },
        ],
    },
    "model3": {
        "title": "At-risk detection approach comparison",
        "metric_labels": ["Accuracy", "Macro F1", "High-risk F1"],
        "why_chosen": (
            "The weighted rule engine stays interpretable for faculty review, avoids black-box "
            "labels without real intervention history, and matches reference risk tiers reliably."
        ),
        "why_useful": (
            "Produces explainable LOW / MEDIUM / HIGH risk levels and indicator breakdowns for "
            "counselling workflows without requiring final exam outcomes."
        ),
        "candidates": [
            {
                "algorithm": "Weighted rule-based engine",
                "selected": True,
                "metrics": {
                    "Accuracy": 0.7485,
                    "Macro F1": 0.7078,
                    "High-risk F1": 0.7216,
                },
            },
            {
                "algorithm": "Logistic Regression",
                "selected": False,
                "metrics": {
                    "Accuracy": 0.7922,
                    "Macro F1": 0.7516,
                    "High-risk F1": 0.7179,
                },
            },
            {
                "algorithm": "Random Forest Classifier",
                "selected": False,
                "metrics": {
                    "Accuracy": 0.8046,
                    "Macro F1": 0.7650,
                    "High-risk F1": 0.7386,
                },
            },
        ],
    },
}
