# Data Pipeline

## Overview

```
Raw Data (student-mat.csv)
    ↓
Loading (pd.read_csv, sep=";")
    ↓
Validation (0 missing values — no cleaning needed)
    ↓
Feature Selection (per model)
    ↓
Preprocessing (embedded in Model 1/2 pipelines)
    ↓
Model Input
    ↓
Prediction / Risk Scoring
    ↓
Structured Output
```

## Raw Data

- **File:** `ml/data/raw/student-mat.csv`
- **Format:** CSV with `;` separator
- **Size:** 395 rows × 33 columns
- **Metadata:** `ml/data/raw/student.txt`

## Loading

```python
import pandas as pd
df = pd.read_csv("data/raw/student-mat.csv", sep=";")
```

Notebooks use Google Colab upload paths (`student_data/student-mat.csv`). For local development, use `ml/data/raw/student-mat.csv`.

## Cleaning

No explicit cleaning is performed in any notebook:

- No `dropna()`, `fillna()`, or outlier removal
- Missing value check confirms 0 nulls across all 33 columns
- No deduplication

## Validation

At inference time, `src/common/validation.py` validates:

- **Models 1 & 2:** All 32 `FEATURE_COLUMNS` present
- **Model 3:** All 5 `RISK_INPUT_FIELDS` present with numeric types and valid ranges

## Feature Engineering

### Model 1

- **Input:** 32 columns (all except `G3`)
- **Target:** `G3`
- No derived features

### Model 2

- **Input:** 32 columns (all except `G3`, `pass_fail`)
- **Target:** `pass_fail` = `"PASS"` if G3 ≥ 10 else `"FAIL"`
- No derived features

### Model 3

- **Input:** `absences`, `G1`, `G2`, `failures`, `studytime`
- **Derived:** `performance_trend = G2 - G1` (computed at scoring time, not stored)
- `G3` explicitly excluded

## Preprocessing (Models 1 and 2)

Embedded in the saved sklearn `Pipeline`:

```python
ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),      # 15 numeric columns
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)  # 17 categorical
    ]
)
```

- Numeric features pass through without scaling
- Categorical features are one-hot encoded
- Unknown categories at inference time are ignored

This preprocessing is **not** repeated at inference — it runs automatically when calling `pipeline.predict()`.

## Model Input

| Model | Input Shape | Source |
|-------|-------------|--------|
| Model 1 | dict with 32 keys → DataFrame (1, 32) | `to_feature_dataframe()` |
| Model 2 | dict with 32 keys → DataFrame (1, 32) | `to_feature_dataframe()` |
| Model 3 | dict with 5 keys | Direct field access |

## Prediction

| Model | Method | Output |
|-------|--------|--------|
| Model 1 | `pipeline.predict(features)` | float (predicted G3) |
| Model 2 | `pipeline.predict()` + `predict_proba()` | PASS/FAIL + probabilities |
| Model 3 | `calculate_risk()` + `get_risk_indicators()` | score, level, indicators |

## Output

Structured Python dictionaries returned by the predictor functions. See [inference.md](inference.md) for contracts.

## Train/Test Split (Training Only)

| Model | Split | Stratify | random_state |
|-------|-------|----------|--------------|
| Model 1 | 80/20 (316 train, 79 test) | No | 42 |
| Model 2 | 80/20 (316 train, 79 test) | Yes (on pass_fail) | 42 |
| Model 3 | N/A (rule-based, no training split) | N/A | N/A |

Model 3 was validated by running against all 395 students and checking consistency with manual test cases.
