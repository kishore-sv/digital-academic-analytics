# ML Architecture

## Overview

The ML module provides three academic intelligence components for PRJ_649. Models 1 and 2 are trained sklearn pipelines; Model 3 is a rule-based risk scoring engine.

```
Student Academic Data (UCI features)
        │
        ▼
   Data Validation
        │
        ├──────────────────┐
        ▼                  ▼
  Model 1              Model 2
  Performance          Pass/Fail
  (Regression)         (Classification)
        │                  │
        ▼                  ▼
  Predicted G3         PASS/FAIL
                       + Probabilities
        │                  │
        └────────┬─────────┘
                 │
    Risk Inputs (5 fields) ──► Model 3
                 │              Risk Engine
                 │              (Rule-based)
                 ▼                  │
           Risk Score + Level ◄─────┘
                 │
                 ▼
        Analytics + Reports
                 │
                 ▼
          FastAPI Backend (planned)
```

## Components

| Component | Type | Artifact | Question Answered |
|-----------|------|----------|-------------------|
| Model 1 | ML regression | `performance_model.pkl` | What final grade is this student likely to achieve? |
| Model 2 | ML classification | `pass_fail_model.pkl` | Is this student likely to pass or fail? |
| Model 3 | Rule-based scoring | `risk_engine_config.json` | Which students are at risk and need attention? |

## Data Flow

1. **Input validation** — `src/common/validation.py` checks required fields and value ranges.
2. **Model 1 / 2** — 32 UCI features are assembled into a DataFrame and passed to the saved sklearn `Pipeline` (preprocessing + model).
3. **Model 3** — Five risk fields are scored using weights and thresholds from the JSON configuration.
4. **Output** — Structured dictionaries returned to the caller (FastAPI backend integration is planned).

## Independence

Models 1, 2, and 3 can run independently. Model 3 does not consume outputs from Models 1 or 2. All three share the same underlying UCI dataset for training/validation but use different input subsets at inference time.

## Key Design Decisions

- **Model 3 is not ML:** The UCI dataset has no historical at-risk labels or intervention outcomes. A transparent rule-based engine was chosen over training a classifier on invented labels.
- **Preprocessing in pipelines:** Models 1 and 2 embed `ColumnTransformer` + `OneHotEncoder` in the saved artifact so inference requires no separate preprocessing step.
- **sklearn version pinning:** Models were trained with scikit-learn 1.6.1; the runtime environment must match.

## Related Documentation

- [models_overview.md](models_overview.md)
- [inference.md](inference.md)
- [data_pipeline.md](data_pipeline.md)
