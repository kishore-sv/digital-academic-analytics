# ML Pipeline

## Overview

The ML layer lives in `ml/` and provides three academic intelligence components trained on the **UCI Student Performance Dataset** (`student-mat.csv`). Inference code is in `ml/src/`; FastAPI integration is planned in `backend/app/ml/`.

For evaluation metrics see [ml-evaluation.md](ml-evaluation.md). For dataset details see [dataset.md](dataset.md). For inference API see [ml/docs/inference.md](../ml/docs/inference.md).

## Pipeline Stages

```
UCI student-mat.csv
    ↓
Load & clean (no nulls)
    ↓
EDA (notebooks)
    ↓
Feature/target split
    ↓
Preprocessing (ColumnTransformer in sklearn Pipeline)
    ↓
Training (80/20 split, random_state=42)
    ↓
Artifact export (.pkl or .json)
    ↓
Python inference (ml/src/)
    ↓
FastAPI integration (planned)
    ↓
Next.js Dashboard
```

## Models

### 1. Student Performance Prediction (Model 1)

- **Type:** Regression (HistGradientBoostingRegressor)
- **Target:** `G3` (final grade, 0–20)
- **Inputs:** 32 UCI features (all columns except `G3`)
- **Output:** `predicted_g3`
- **Artifact:** `ml/models/model_1/performance_model.pkl`
- **Metrics:** MAE 1.2321, RMSE 1.9348, R² 0.8174

### 2. Pass/Fail Prediction (Model 2)

- **Type:** Binary classification (Logistic Regression)
- **Target:** `pass_fail` (PASS if G3 ≥ 10)
- **Inputs:** 32 UCI features (excludes `G3`)
- **Output:** `PASS`/`FAIL` + pass/fail probabilities
- **Artifact:** `ml/models/model_2/pass_fail_model.pkl`
- **Metrics:** Accuracy 0.8861, FAIL Recall 0.9231, FAIL F1 0.8421, ROC-AUC 0.9652

### 3. At-Risk Detection (Model 3)

- **Type:** Rule-based weighted risk engine (**not ML**)
- **Inputs:** `absences`, `G1`, `G2`, `failures`, `studytime` (no G3)
- **Output:** `risk_score` (0–100), `risk_level` (LOW/MEDIUM/HIGH), `risk_indicators`
- **Artifact:** `ml/models/model_3/risk_engine_config.json`

## Development Location

| Stage | Location |
|-------|----------|
| Raw data | `ml/data/raw/student-mat.csv` |
| Notebooks | `ml/notebooks/model_{1,2,3}/` |
| Inference | `ml/src/` |
| Trained models | `ml/models/model_{1,2,3}/` |
| Backend integration | `backend/app/ml/` (stub) |

## ERP Field Mapping (Future)

Current models use UCI columns (`G1`, `G2`, `absences`, etc.). ERP fields such as attendance %, internal marks, and CGPA require retraining when institutional data is available.

## Related Documentation

- [Dataset](dataset.md)
- [ML Evaluation](ml-evaluation.md)
- [ML README](../ml/README.md)
- [ML Architecture](../ml/docs/ml_architecture.md)
- [Architecture](architecture.md)
- [Development Phases](development-phases.md)
