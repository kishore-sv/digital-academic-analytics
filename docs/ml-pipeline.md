# ML Pipeline

## Overview

The project uses three finalized ML components trained on **synthetic CBCS university data**. These models are **not real-world validated** — they are ML-powered academic predictions based on the trained project models.

## Artifacts

All artifacts live in `ml/models/`:

| File | Component | Type |
|------|-----------|------|
| `model1_endterm_histgradientboosting.pkl` | End-term mark prediction | HistGradientBoostingRegressor |
| `model2_pass_fail_histgradientboosting.pkl` | Pass/fail prediction | HistGradientBoostingClassifier |
| `model3_risk_engine_config.json` | At-risk detection | Rule-based weighted scoring engine |
| `model1_metrics.json` | Model 1 evaluation metrics | JSON |
| `model2_metrics.json` | Model 2 evaluation metrics | JSON |
| `model3_metrics.json` | Model 3 evaluation metrics | JSON |

## Model 1 — Performance Prediction

**Algorithm:** HistGradientBoostingRegressor

**Features:** CA_mark, MID_mark, attendance_percentage, study_hours_per_week, assignment_completion_pct, previous_sgpa, previous_cgpa, backlog_count, course_credits, course_type, branch, semester

**Output:** `predicted_end_marks` (0–100)

**Metrics:** MAE 5.63, RMSE 7.07, R² 0.764

## Model 2 — Pass/Fail Prediction

**Algorithm:** HistGradientBoostingClassifier (selected for FAIL recall and ROC-AUC)

**Features:** Same as Model 1 minus course_type

**Output:** prediction (PASS/FAIL), pass_probability, fail_probability

**Metrics:** Accuracy 95.3%, FAIL recall 96.7%, ROC-AUC 0.991

## Model 3 — At-Risk Detection

**Type:** Rule-based weighted scoring engine (NOT ML)

**Features and weights:**
- attendance_percentage: 20%
- previous_cgpa: 20%
- backlog_count: 20%
- current_failed_courses: 15%
- low_performance_course_count: 10%
- study_hours_per_week: 5%
- assignment_completion_percentage: 5%
- performance_trend: 5%

**Risk thresholds:**
- LOW: score ≤ 22
- MEDIUM: 22 < score ≤ 38
- HIGH: score > 38

## Backend Integration

Models are loaded once at FastAPI startup via `ModelLoader` in `backend/app/ml/model_loader.py`.

Inference services:
- `backend/app/ml/model1.py` — performance prediction
- `backend/app/ml/model2.py` — pass/fail prediction
- `backend/app/ml/risk_engine.py` — risk scoring (reads config JSON)

**Important:** scikit-learn is pinned to 1.6.1 for pickle compatibility.

## API Endpoints

```
POST /api/v1/predictions/performance
POST /api/v1/predictions/pass-fail
POST /api/v1/predictions/risk
POST /api/v1/predictions/all
POST /api/v1/predictions/student  (requires auth, uses DB features)
```
