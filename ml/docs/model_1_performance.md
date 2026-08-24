# Model 1 — Student Performance Prediction

## 1. Purpose

Predict a student's final academic performance (final grade G3) from demographic and academic information available before the final exam.

**Question answered:** "What final grade is this student likely to achieve?"

## 2. Problem Definition

- **Type:** Regression
- **Target:** `G3` (final grade, scale 0–20)

## 3. Dataset

UCI Student Performance Dataset — Mathematics course.

- **File:** `student-mat.csv`
- **Size:** 395 students, 33 columns
- **Local path:** `ml/data/raw/student-mat.csv`

## 4. Dataset Source

UCI Machine Learning Repository. Notebooks load the dataset from a Google Colab upload (`student+performance.zip` → `student_data/student-mat.csv`).

## 5. Input Features

32 features (all columns except `G3`):

**Numerical (15):** `age`, `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`, `G1`, `G2`

**Categorical (17):** `school`, `sex`, `address`, `famsize`, `Pstatus`, `Mjob`, `Fjob`, `reason`, `guardian`, `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic`

## 6. Target Variable

`G3` — final grade (0–20).

## 7. Data Cleaning

No explicit cleaning steps in the notebook. Exploratory checks only:

- `df.info()`, `df.isnull().sum()`, `df.describe()`
- Grade correlation: `df[["G1", "G2", "G3"]].corr()`
- Missing values: 0 for all columns

## 8. EDA

- Dataset shape and column types inspected
- Correlation between G1, G2, G3 examined
- G3 value distribution reviewed via `value_counts()`

## 9. Feature Engineering

No additional feature engineering beyond using raw columns. Preprocessing is handled inside the sklearn `Pipeline`.

## 10. Algorithms Compared

| Algorithm | Hyperparameters |
|-----------|-----------------|
| Linear Regression | defaults |
| Random Forest Regressor | `n_estimators=300`, `random_state=42`, `n_jobs=-1` |
| HistGradientBoostingRegressor | `random_state=42` |

No hyperparameter tuning or grid search.

## 11. Training Process

1. Load `student-mat.csv` with `sep=";"`
2. Split features (`X`) and target (`y = G3`)
3. `train_test_split(X, y, test_size=0.20, random_state=42)` — no stratification
4. Build `ColumnTransformer` preprocessor for each model
5. Train three `Pipeline` objects (preprocessor + estimator)
6. Evaluate on held-out test set (79 samples)

## 12. Evaluation Metrics

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (coefficient of determination)

## 13. Model Comparison

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| HistGradientBoosting | 1.2321 | 1.9348 | 0.8174 |
| Random Forest | 1.1863 | 2.0023 | 0.8045 |
| Linear Regression | 1.6467 | 2.3784 | 0.7241 |

Results sorted by RMSE in the notebook.

## 14. Selected Model

**HistGradientBoostingRegressor**

## 15. Why the Selected Model Was Chosen

Lowest RMSE on the test set (1.9348). The notebook selects by RMSE ranking; no additional prose justification is provided.

## 16. Model File

- **Path:** `ml/models/model_1/performance_model.pkl`
- **Format:** joblib pickle
- **Contents:** `sklearn.pipeline.Pipeline` with steps `preprocessor` (ColumnTransformer) and `model` (HistGradientBoostingRegressor)
- **Training sklearn version:** 1.6.1

## 17. Input Contract

All 32 UCI feature fields are required. See `src/common/features.py` for the full list.

| Field | Type | Required | Valid Range / Values |
|-------|------|----------|----------------------|
| school | string | yes | GP, MS |
| sex | string | yes | F, M |
| age | int | yes | 15–22 |
| address | string | yes | U, R |
| famsize | string | yes | LE3, GT3 |
| Pstatus | string | yes | T, A |
| Medu | int | yes | 0–4 |
| Fedu | int | yes | 0–4 |
| Mjob, Fjob, reason, guardian | string | yes | See student.txt |
| traveltime | int | yes | 1–4 |
| studytime | int | yes | 1–4 |
| failures | int | yes | ≥ 0 |
| schoolsup, famsup, paid, activities, nursery, higher, internet, romantic | string | yes | yes, no |
| famrel, freetime, goout, Dalc, Walc, health | int | yes | 1–5 |
| absences | int | yes | ≥ 0 |
| G1, G2 | float/int | yes | 0–20 |

Preprocessing (OneHotEncoder) is applied automatically by the saved pipeline.

## 18. Output Contract

```json
{
  "predicted_g3": 13.7
}
```

- `predicted_g3`: float — predicted final grade (typically 0–20 range)

## 19. Inference Flow

```
Input dict (32 fields)
    → validate_uci_features()
    → to_feature_dataframe() → single-row DataFrame
    → joblib.load("performance_model.pkl")
    → pipeline.predict(features)
    → {"predicted_g3": float}
```

Entry point: `src/model_1/predictor.py` → `predict_performance(input_data)`

## 20. Limitations

- Trained on a single UCI dataset (395 Portuguese students, Mathematics course only)
- No cross-validation; single 80/20 split
- No hyperparameter tuning
- Categorical encoding depends on categories seen during training; unknown categories are ignored (`handle_unknown="ignore"`)
- Requires scikit-learn 1.6.1 for reliable pickle loading

## 21. Future Improvements

- Cross-validation for more robust metric estimates
- Hyperparameter tuning for HistGradientBoosting
- Evaluate on Portuguese course data (`student-por.csv`) or combined dataset
- Retrain when institutional data becomes available
