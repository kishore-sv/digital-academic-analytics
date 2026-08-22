# ML Evaluation, Versioning, and Explainability

This document defines evaluation metrics, class imbalance handling, model versioning, and explainability requirements for all three ML models.

**Models have not been trained yet.**

## Train/Test Split

- **80% training / 20% test** for all models
- **Stratified split** by outcome class for at-risk and pass/fail models (preserves class proportions)
- Random seed fixed (`random_state=42`) for reproducibility
- No data from the test set used during training or hyperparameter tuning

## Evaluation Metrics by Model

| Model | Type | Primary metrics | Secondary metrics |
|-------|------|----------------|-------------------|
| Performance prediction | Regression | MAE, RMSE | R² |
| At-risk detection | Classification | **Recall, F1** | Precision, AUC-ROC |
| Pass/fail prediction | Classification | **Recall, F1, AUC-ROC** | Precision |

### Why Recall and F1 for Classification Models

In academic intervention systems, **false negatives are worse than false positives**:

- **False negative** (at-risk): A struggling student is not flagged → no intervention → potential academic failure
- **False positive** (at-risk): A student is flagged but is actually fine → unnecessary check-in (low cost)

Accuracy alone is misleading when at-risk students are a minority class (typically 10–20% of a cohort). A model predicting "not at-risk" for everyone would score 80–90% accuracy while missing every struggling student.

**Target thresholds (guidelines):**
- At-risk recall: ≥ 0.80 (catch at least 80% of at-risk students)
- At-risk F1: ≥ 0.70
- Pass/fail recall: ≥ 0.85

## Class Imbalance Handling

At-risk and pass/fail datasets are typically imbalanced (minority class = at-risk or failing students).

### Training Strategy

```python
# Planned approach in train_risk.py and train_pass_fail.py
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    class_weight="balanced",  # auto-adjust weights inversely proportional to class frequency
    random_state=42,
)
```

### Evaluation Strategy

- Report **precision-recall curve** alongside ROC curve
- Report per-class precision, recall, and F1 (not just aggregate)
- Never report accuracy as the primary metric for imbalanced models
- Document class distribution in the metrics JSON file

## Model Versioning

Models must never be silently overwritten. Each training run produces a new versioned artifact.

### Directory Structure

```
ml/models/
├── performance_v1.pkl
├── performance_v1_metrics.json
├── risk_v1.pkl
├── risk_v1_metrics.json
├── pass_fail_v1.pkl
└── pass_fail_v1_metrics.json
```

### Metrics JSON Schema

```json
{
  "model": "risk",
  "version": 1,
  "trained_at": "2026-04-15T10:30:00Z",
  "dataset_hash": "sha256:abc123...",
  "train_size": 1600,
  "test_size": 400,
  "metrics": {
    "recall": 0.83,
    "f1": 0.74,
    "precision": 0.67,
    "auc_roc": 0.89
  },
  "class_distribution": {
    "low": 0.65,
    "medium": 0.20,
    "high": 0.15
  },
  "hyperparameters": {
    "class_weight": "balanced",
    "n_estimators": 100
  }
}
```

### Versioning Rules

- Increment version on every retrain: `risk_v1.pkl` → `risk_v2.pkl`
- Never delete old versions until the new version is validated and deployed
- Backend reads active version from environment: `RISK_MODEL_VERSION=1`
- Document which version is active in `ml/models/ACTIVE_VERSIONS.json`

## Explainability (SHAP)

For at-risk and pass/fail predictions, the system must explain **why** a student was flagged. This is required for:
- Faculty trust and appropriate intervention
- Parent communication
- Project defense / viva

### Approach

- Use **SHAP** (SHapley Additive exPlanations) via the `shap` library
- Compute SHAP values at inference time for each prediction
- Return top-3 contributing features in the API response

### API Response Format (planned)

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

Negative impact = pushes toward at-risk. Positive impact = pushes toward safe.

### SHAP Install (future)

```bash
cd ml && uv add shap
cd backend && uv add shap
```

## Related Documentation

- [ML Pipeline](ml-pipeline.md)
- [Dataset](dataset.md)
- [Development Phases](development-phases.md)
- [Reports](reports.md) (SHAP factors included in at-risk PDF reports)
