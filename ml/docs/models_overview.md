# Models Overview

Summary of the three academic intelligence components.

## Comparison Table

| | Model 1 | Model 2 | Model 3 |
|---|---------|---------|---------|
| **Name** | Student Performance Prediction | Student Pass/Fail Prediction | Student At-Risk Detection |
| **Problem type** | Regression | Binary classification | Rule-based risk scoring |
| **Algorithm** | HistGradientBoostingRegressor | LogisticRegression | Weighted threshold rules |
| **Dataset** | UCI student-mat.csv (395 rows) | Same | Same (for validation only) |
| **Input count** | 32 features | 32 features | 5 fields |
| **Target** | G3 (0–20) | pass_fail (PASS/FAIL) | N/A |
| **Artifact** | `performance_model.pkl` | `pass_fail_model.pkl` | `risk_engine_config.json` |
| **Serialization** | joblib pickle (sklearn Pipeline) | joblib pickle (sklearn Pipeline) | JSON configuration |
| **Primary metric** | RMSE (selection), R² | F1 for FAIL class | N/A (no formal evaluation) |
| **Notebook** | `notebooks/model_1/performance_model.ipynb` | `notebooks/model_2/pass_fail_model.ipynb` | `notebooks/model_3/risk_model.ipynb` |
| **Inference function** | `predict_performance()` | `predict_pass_fail()` | `assess_student_risk()` |

## Input Summary

### Models 1 and 2 (32 UCI features)

`school`, `sex`, `age`, `address`, `famsize`, `Pstatus`, `Medu`, `Fedu`, `Mjob`, `Fjob`, `reason`, `guardian`, `traveltime`, `studytime`, `failures`, `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`, `G1`, `G2`

Model 2 excludes `G3` (used only to derive the training target).

### Model 3 (5 fields)

`absences`, `G1`, `G2`, `failures`, `studytime`

`G3` is explicitly excluded from risk assessment.

## Output Summary

| Model | Output |
|-------|--------|
| Model 1 | `{"predicted_g3": float}` |
| Model 2 | `{"prediction": "PASS"\|"FAIL", "pass_probability": float, "fail_probability": float}` |
| Model 3 | `{"risk_score": float, "risk_level": "LOW"\|"MEDIUM"\|"HIGH", "risk_indicators": list, "component_risks": dict}` |

## When to Use Each Model

- **Model 1** — Estimate a student's expected final grade based on current academic and demographic data.
- **Model 2** — Classify whether a student is likely to pass or fail, with probability estimates.
- **Model 3** — Flag students who may need academic intervention based on attendance, performance trend, failures, and study habits.
