# Model Evaluation

Metrics below are from the Colab notebooks on the UCI `student-mat.csv` test split (80/20, `random_state=42`).

## Model 1 — Performance Prediction (Regression)

| Metric | Value |
|--------|-------|
| MAE | 1.2321 |
| RMSE | 1.9348 |
| R² | 0.8174 |

**Algorithm:** HistGradientBoostingRegressor  
**Split:** No stratification

## Model 2 — Pass/Fail Prediction (Classification)

| Metric | Value |
|--------|-------|
| Accuracy | 0.8861 |
| Precision (FAIL) | 0.7742 |
| Recall (FAIL) | 0.9231 |
| F1 (FAIL) | 0.8421 |
| ROC-AUC | 0.9652 |

**Algorithm:** Logistic Regression  
**Split:** Stratified by `pass_fail`

FAIL recall is the primary metric for early-warning — the model catches 24 of 26 actual FAIL students in the test set.

## Model 3 — At-Risk Detection (Rule Engine)

Model 3 has **no formal ML evaluation** — it is a heuristic rule engine, not a trained classifier.

### Distribution on Full Dataset (395 students)

| Level | Count | % |
|-------|-------|---|
| LOW | 165 | 41.77% |
| MEDIUM | 151 | 38.23% |
| HIGH | 79 | 20.00% |

### Score Statistics

| Stat | Value |
|------|-------|
| Mean | 39.49 |
| Median | 35.00 |
| Min | 0 |
| Max | 100 |

### Validation Checks

- G3 leakage test passed (changing G3 does not affect risk output)
- Config JSON reload verified

## Caveats

- 395 students is a small dataset — test metrics should not be treated as production guarantees.
- UCI domain may not match institutional ERP data — retrain and re-evaluate on real data when available.
- Model 3 thresholds are expert/heuristic, not ML-optimized.

## Running Tests

```bash
cd ml && uv sync && uv run pytest
```

Tests verify model loading, prediction output shape/range, and risk engine behavior.
