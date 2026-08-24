# Model Evaluation

Evaluation results are taken directly from the training notebooks. No metrics were fabricated or re-computed outside the notebooks.

## Model 1 — Performance Prediction (Regression)

### Metrics Used

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (coefficient of determination)

### Algorithms Compared

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| HistGradientBoostingRegressor | 1.2321 | 1.9348 | 0.8174 |
| RandomForestRegressor | 1.1863 | 2.0023 | 0.8045 |
| LinearRegression | 1.6467 | 2.3784 | 0.7241 |

### Best Model

**HistGradientBoostingRegressor** — selected by lowest RMSE.

### Final Test Performance

```
MAE  : 1.2321
RMSE : 1.9348
R²   : 0.8174
```

### Evaluation Approach

- Single 80/20 train/test split (`random_state=42`, no stratification)
- No cross-validation
- No hyperparameter tuning

---

## Model 2 — Pass/Fail Prediction (Classification)

### Metrics Used

- Accuracy
- Precision (FAIL as positive class)
- Recall (FAIL)
- F1 (FAIL)
- ROC-AUC (binary: FAIL=1)

### Algorithms Compared

| Model | Accuracy | Precision (FAIL) | Recall (FAIL) | F1 (FAIL) | ROC-AUC |
|-------|----------|------------------|---------------|-----------|---------|
| LogisticRegression | 0.8861 | 0.7742 | 0.9231 | 0.8421 | 0.9652 |
| RandomForestClassifier | 0.8734 | 0.7500 | 0.9231 | 0.8276 | 0.9376 |
| HistGradientBoostingClassifier | 0.8734 | 0.7500 | 0.9231 | 0.8276 | 0.9565 |

### Best Model

**LogisticRegression** — selected by highest F1 for FAIL class.

### Final Test Performance

```
Accuracy  : 0.8861
Precision : 0.7742 (FAIL)
Recall    : 0.9231 (FAIL)
F1 Score  : 0.8421 (FAIL)
ROC-AUC   : 0.9652
```

### Confusion Matrix (Logistic Regression, test set)

```
              Predicted
              FAIL  PASS
Actual FAIL    24     2
Actual PASS     7    46
```

FAIL recall: 24/26 = 92.31% — identified 24 of 26 actual FAIL students in the test set.

### Evaluation Approach

- Single 80/20 stratified train/test split (`random_state=42`)
- No cross-validation
- No hyperparameter tuning
- FAIL class prioritized for early-warning use case

---

## Model 3 — Risk Assessment (Rule-Based)

### Formal Evaluation

**No formal ML evaluation exists.** Model 3 is a deterministic rule-based engine, not a trained classifier.

### Validation Performed

The notebook includes manual/deterministic checks:

1. **EDA:** Distribution of input fields and derived trends
2. **Per-factor distributions:** Value counts for each `*_risk` tier column
3. **Consistency check:** `calculate_risk()` on first row matches precomputed dataframe values (47.50, MEDIUM)
4. **Synthetic test cases:**
   - Low-risk student → score 0.0, LOW
   - Medium-risk student → score 60.0, MEDIUM
   - High-risk student → score 100.0, HIGH
5. **G3 independence:** Same inputs with different G3 produce identical risk results
6. **Batch validation:** All 395 students scored; distribution reported
7. **Config round-trip:** JSON save/load equality verified

### Dataset Distribution (395 students)

| Risk Level | Count | Percentage |
|------------|-------|------------|
| LOW | 165 | 41.77% |
| MEDIUM | 151 | 38.23% |
| HIGH | 79 | 20.00% |

Risk score statistics: mean 39.49, median 35.00, min 0, max 100.

### Future Evaluation

When institutional at-risk labels or intervention outcomes become available, the risk engine thresholds and weights should be validated against real outcomes.
