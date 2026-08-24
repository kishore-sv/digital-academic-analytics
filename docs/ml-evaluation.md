# ML Evaluation

Evaluation metrics for the three academic intelligence components, derived from Colab notebook training on the UCI `student-mat.csv` dataset.

## Train/Test Split

| Model | Split | Stratify | random_state |
|-------|-------|----------|--------------|
| Model 1 (regression) | 80/20 | No | 42 |
| Model 2 (classification) | 80/20 | Yes (`pass_fail`) | 42 |
| Model 3 (rule engine) | Full dataset validation | N/A | N/A |

## Model 1 — Performance Prediction (Regression)

| Metric | Value |
|--------|-------|
| MAE | 1.2321 |
| RMSE | 1.9348 |
| R² | 0.8174 |

**Algorithm:** HistGradientBoostingRegressor in sklearn Pipeline

## Model 2 — Pass/Fail Prediction (Classification)

| Metric | Value |
|--------|-------|
| Accuracy | 0.8861 |
| Precision (FAIL) | 0.7742 |
| Recall (FAIL) | 0.9231 |
| F1 (FAIL) | 0.8421 |
| ROC-AUC | 0.9652 |

**Algorithm:** Logistic Regression in sklearn Pipeline

### Why FAIL Recall Matters

In academic intervention systems, missing a failing student (false negative) is worse than a false alarm. The selected model catches **24 of 26** actual FAIL students in the test set (92.31% recall).

### Class Distribution

- PASS: 265 (67.09%)
- FAIL: 130 (32.91%)

## Model 3 — At-Risk Detection (Rule Engine)

Model 3 is **not** an ML classifier and has no formal ML metrics. It is a transparent heuristic risk engine.

### Distribution on Full Dataset (395 students)

| Level | Count | % |
|-------|-------|---|
| LOW | 165 | 41.77% |
| MEDIUM | 151 | 38.23% |
| HIGH | 79 | 20.00% |

### Validation

- G3 leakage test passed (risk output unchanged when G3 varies)
- Config JSON weights/thresholds verified on reload

## Caveats

- **395 students** is a small dataset — test metrics are not production guarantees.
- **UCI domain** may not match institutional ERP data.
- **Model 3 weights** are heuristic, not ML-optimized.

## Running Tests

```bash
cd ml && uv sync && uv run pytest
```

## Future: Explainability

SHAP explainability for classification models is a future enhancement when FastAPI integration is implemented. Model 3 already provides human-readable `risk_indicators`.

## Related Documentation

- [ML Pipeline](ml-pipeline.md)
- [Dataset](dataset.md)
- [Model Evaluation (ml/)](../ml/docs/model_evaluation.md)
- [Development Phases](development-phases.md)
