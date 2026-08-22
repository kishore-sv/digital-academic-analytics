# ML Pipeline

## Overview

The ML pipeline is developed separately in the `ml/` directory and integrated into the FastAPI backend for inference.

**Models have not been trained yet.** This document describes the planned pipeline and model specifications.

For evaluation metrics, class imbalance handling, explainability, and versioning, see [ml-evaluation.md](ml-evaluation.md).

For the dataset strategy (the first blocking task), see [dataset.md](dataset.md).

## Pipeline Stages

```
Dataset (synthetic_academic_data.csv)
    ↓
Data Cleaning
    ↓
EDA (Exploratory Data Analysis)
    ↓
Feature Engineering
    ↓
Training (stratified 80/20 split)
    ↓
Evaluation (metrics per model type)
    ↓
Versioned Pickle Model + metrics JSON
    ↓
FastAPI Inference (with SHAP explainability)
    ↓
Next.js Dashboard
```

## Planned Models

### 1. Student Performance Prediction

**Inputs:**
- Attendance percentage (computed from raw records)
- Internal marks
- Assignment marks
- Previous GPA/CGPA
- Previous semester marks
- Backlogs
- Academic history

**Outputs:**
- Predicted final marks
- Predicted grade
- Performance category

**Artifact:** `ml/models/performance_v1.pkl` + `performance_v1_metrics.json`
**Metrics:** MAE, RMSE, R²

### 2. At-Risk Student Detection

**Inputs:**
- Attendance percentage
- Internal marks
- Previous CGPA
- Backlogs
- Assignment performance
- Previous results

**Outputs:**
- Low / Medium / High risk
- Risk probability
- Top-3 SHAP contributing factors

**Artifact:** `ml/models/risk_v1.pkl` + `risk_v1_metrics.json`
**Metrics:** Recall, F1 (primary); Precision, AUC-ROC (secondary)
**Class imbalance:** `class_weight='balanced'`

### 3. Pass/Fail Prediction

**Inputs:**
- Attendance percentage
- Internal marks
- Previous CGPA
- Assignment marks
- Backlogs
- Academic history

**Outputs:**
- Pass / Fail
- Probability
- Top-3 SHAP contributing factors

**Artifact:** `ml/models/pass_fail_v1.pkl` + `pass_fail_v1_metrics.json`
**Metrics:** Recall, F1, AUC-ROC

## Model Versioning

Models are never silently overwritten. Each training run produces a new version:

```
ml/models/
├── performance_v1.pkl
├── performance_v1_metrics.json
├── risk_v1.pkl
├── risk_v1_metrics.json
├── pass_fail_v1.pkl
└── pass_fail_v1_metrics.json
```

Active version is configured via environment variables (`RISK_MODEL_VERSION=1`, etc.).

## Inference Response (with Explainability)

At-risk and pass/fail predictions include SHAP top factors:

```json
{
  "student_id": "uuid",
  "risk_level": "high",
  "risk_probability": 0.87,
  "top_factors": [
    { "feature": "attendance_percentage", "impact": -0.31, "value": 62.0 },
    { "feature": "internal_marks_avg", "impact": -0.22, "value": 45.0 },
    { "feature": "backlogs", "impact": -0.18, "value": 2 }
  ]
}
```

## Development Location

| Stage | Location |
|-------|----------|
| Raw data | `ml/datasets/raw/` |
| Processed data | `ml/datasets/processed/` |
| Notebooks | `ml/notebooks/` |
| Training scripts | `ml/src/` |
| Trained models | `ml/models/` (versioned) |
| Inference | `backend/app/ml/` |

## Related Documentation

- [Dataset](dataset.md)
- [ML Evaluation](ml-evaluation.md)
- [Architecture](architecture.md)
- [Development Phases](development-phases.md)
- [Reports](reports.md)
