# PRJ_649 ML Development

Machine learning development for academic performance prediction, at-risk detection, and pass/fail prediction.

## Setup

```bash
uv sync
```

## First Task: Generate Synthetic Dataset

`ml/datasets/raw/` is currently empty. This blocks all ML training and analytics dashboard development.

```bash
# Future implementation:
uv run python src/generate_synthetic.py
# Output: ml/datasets/raw/synthetic_academic_data.csv
```

See [docs/dataset.md](../docs/dataset.md) for the full dataset schema and generation rules.

## Structure

```
ml/
├── datasets/
│   ├── raw/             # Raw academic datasets (currently empty)
│   └── processed/       # Cleaned train/test splits
├── notebooks/           # Jupyter notebooks for EDA and experimentation
├── src/                 # Training and evaluation scripts
└── models/              # Versioned pickle models (not yet created)
    ├── performance_v1.pkl
    ├── performance_v1_metrics.json
    ├── risk_v1.pkl
    ├── risk_v1_metrics.json
    └── ...
```

## Planned Models

### 1. Performance Prediction
- **Inputs:** Attendance %, internal marks, assignment marks, CGPA, backlogs, academic history
- **Outputs:** Predicted final marks, predicted grade, performance category
- **Metrics:** MAE, RMSE, R²

### 2. At-Risk Student Detection
- **Inputs:** Attendance %, internal marks, CGPA, backlogs, assignment performance
- **Outputs:** Low / Medium / High risk, risk probability, top-3 SHAP factors
- **Metrics:** Recall, F1 (primary — false negatives are worse than false positives)

### 3. Pass/Fail Prediction
- **Inputs:** Attendance %, internal marks, CGPA, assignment marks, backlogs
- **Outputs:** Pass / Fail, probability, top-3 SHAP factors
- **Metrics:** Recall, F1, AUC-ROC

## Model Versioning

Models are never silently overwritten. Each training run produces a new version:

```
risk_v1.pkl  +  risk_v1_metrics.json
risk_v2.pkl  +  risk_v2_metrics.json  (after retrain)
```

Active version configured via `RISK_MODEL_VERSION=1` environment variable.

## Evaluation

- 80/20 stratified train/test split
- `class_weight='balanced'` for at-risk and pass/fail models
- SHAP explainability for classification predictions

See [docs/ml-evaluation.md](../docs/ml-evaluation.md) for full metrics specification.

## Note

Models have not been trained yet. Generate the synthetic dataset first (Phase 1), then proceed with EDA and training.

## Related Documentation

- [Dataset Strategy](../docs/dataset.md)
- [ML Pipeline](../docs/ml-pipeline.md)
- [ML Evaluation](../docs/ml-evaluation.md)
- [Development Phases](../docs/development-phases.md)
