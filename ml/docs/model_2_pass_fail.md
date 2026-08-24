# Model 2 — Student Pass/Fail Prediction

## 1. Purpose

Predict whether a student is likely to pass or fail based on academic and demographic information available before the final exam.

**Question answered:** "Is this student likely to pass or fail?"

## 2. Problem Definition

- **Type:** Binary classification
- **Classes:** `PASS`, `FAIL`
- **Positive class for evaluation:** `FAIL` (early-warning use case)

## 3. Dataset

UCI Student Performance Dataset — Mathematics course.

- **File:** `student-mat.csv`
- **Size:** 395 students, 33 columns
- **Local path:** `ml/data/raw/student-mat.csv`

## 4. Dataset Source

UCI Machine Learning Repository. Loaded in Google Colab from uploaded zip archive.

## 5. Input Features

32 features — all columns except `G3` and `pass_fail`:

**Numerical (15):** `age`, `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`, `G1`, `G2`

**Categorical (17):** `school`, `sex`, `address`, `famsize`, `Pstatus`, `Mjob`, `Fjob`, `reason`, `guardian`, `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic`

`G3` is excluded from inputs (used only to derive the training target).

## 6. Target Variable

`pass_fail` — derived from G3:

```python
df["pass_fail"] = df["G3"].apply(lambda grade: "PASS" if grade >= 10 else "FAIL")
```

**Distribution:**

| Class | Count | Percentage |
|-------|-------|------------|
| PASS | 265 | 67.09% |
| FAIL | 130 | 32.91% |

## 7. Data Cleaning

No explicit cleaning. 0 missing values across all columns.

## 8. Feature Engineering

No additional feature engineering. Preprocessing is embedded in the sklearn `Pipeline`.

## 9. Algorithms Compared

| Algorithm | Hyperparameters |
|-----------|-----------------|
| Logistic Regression | `max_iter=1000`, `random_state=42` |
| Random Forest Classifier | `n_estimators=300`, `random_state=42`, `n_jobs=-1` |
| HistGradientBoostingClassifier | `random_state=42` |

No hyperparameter tuning.

## 10. Training Process

1. Load `student-mat.csv` with `sep=";"`
2. Derive `pass_fail` target from G3
3. `X = df.drop(columns=["G3", "pass_fail"])`, `y = df["pass_fail"]`
4. `train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)`
5. Train three `Pipeline` objects
6. Evaluate on test set (79 samples: 53 PASS, 26 FAIL)

## 11. Evaluation Metrics

- Accuracy
- Precision (FAIL)
- Recall (FAIL)
- F1 (FAIL)
- ROC-AUC (binary: FAIL=1, PASS=0)

## 12. Model Comparison

| Model | Accuracy | Precision (FAIL) | Recall (FAIL) | F1 (FAIL) | ROC-AUC |
|-------|----------|------------------|---------------|-----------|---------|
| Logistic Regression | 0.8861 | 0.7742 | 0.9231 | 0.8421 | 0.9652 |
| Random Forest | 0.8734 | 0.7500 | 0.9231 | 0.8276 | 0.9376 |
| HistGradientBoosting | 0.8734 | 0.7500 | 0.9231 | 0.8276 | 0.9565 |

Sorted by F1 (FAIL) in the notebook.

## 13. Selected Model

**Logistic Regression** — highest F1 for the FAIL class.

**Confusion matrix (test set):**

|  | Pred FAIL | Pred PASS |
|---|-----------|-----------|
| Actual FAIL | 24 | 2 |
| Actual PASS | 7 | 46 |

FAIL recall: 24/26 = 92.31%

## 14. Model File

- **Path:** `ml/models/model_2/pass_fail_model.pkl`
- **Format:** joblib pickle
- **Contents:** `sklearn.pipeline.Pipeline` with `preprocessor` + `LogisticRegression`
- **Classes:** `['FAIL', 'PASS']` (sklearn alphabetical order)
- **Training sklearn version:** 1.6.1

## 15. Input Contract

Same 32 UCI features as Model 1. See `src/common/features.py` and [model_1_performance.md](model_1_performance.md#17-input-contract).

## 16. Output Contract

```json
{
  "prediction": "PASS",
  "pass_probability": 0.9999,
  "fail_probability": 0.0001
}
```

| Field | Type | Description |
|-------|------|-------------|
| prediction | string | `"PASS"` or `"FAIL"` |
| pass_probability | float | Model-estimated probability of PASS (0–1) |
| fail_probability | float | Model-estimated probability of FAIL (0–1) |

Probabilities sum to 1.0. These are model estimates, not guaranteed real-world probabilities.

## 17. Inference Flow

```
Input dict (32 fields)
    → validate_uci_features()
    → to_feature_dataframe()
    → joblib.load("pass_fail_model.pkl")
    → pipeline.predict() + pipeline.predict_proba()
    → {"prediction", "pass_probability", "fail_probability"}
```

Entry point: `src/model_2/predictor.py` → `predict_pass_fail(input_data)`

## 18. Limitations

- PASS/FAIL threshold (G3 ≥ 10) is a project assumption, not an institutional policy
- Class imbalance (67% PASS) — stratified split used but no `class_weight` tuning
- Single train/test split, no cross-validation
- Requires scikit-learn 1.6.1 for pickle loading
- Trained on UCI dataset only

## 19. Future Improvements

- Cross-validation and class-weight tuning
- Calibrate probability outputs
- Evaluate threshold sensitivity for PASS/FAIL definition
- Retrain on institutional data when available
