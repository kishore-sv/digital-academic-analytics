# Inference

How to use the ML module for prediction and how the FastAPI backend will eventually consume it.

## Python API

### Model 1 — Performance Prediction

```python
from src.model_1.predictor import predict_performance

result = predict_performance({
    "school": "GP", "sex": "F", "age": 17, "address": "U",
    # ... all 32 UCI features (see src/common/features.py)
    "absences": 4, "G1": 12, "G2": 13
})
# {"predicted_g3": 13.7}
```

### Model 2 — Pass/Fail Prediction

```python
from src.model_2.predictor import predict_pass_fail

result = predict_pass_fail({...})  # same 32 features
# {
#   "prediction": "PASS",
#   "pass_probability": 0.9999,
#   "fail_probability": 0.0001
# }
```

### Model 3 — Risk Assessment

```python
from src.model_3.risk_engine import assess_student_risk

result = assess_student_risk({
    "absences": 6,
    "G1": 10,
    "G2": 9,
    "failures": 1,
    "studytime": 2
})
# {
#   "risk_score": 47.5,
#   "risk_level": "MEDIUM",
#   "risk_indicators": ["Moderate Absence", "Low Current Performance", ...],
#   "component_risks": {"absence_risk": 1, "performance_risk": 2, ...}
# }
```

## Model Loading

Models are loaded lazily on first prediction call and cached in module-level variables.

| Model | Loader | Path |
|-------|--------|------|
| Model 1 | `joblib.load()` | `ml/models/model_1/performance_model.pkl` |
| Model 2 | `joblib.load()` | `ml/models/model_2/pass_fail_model.pkl` |
| Model 3 | `json.load()` | `ml/models/model_3/risk_engine_config.json` |

Path resolution is handled by `src/common/paths.py`.

### sklearn Version Requirement

Models 1 and 2 were trained with **scikit-learn 1.6.1**. The project pins this version. Loading with a different version may produce:

```
InconsistentVersionWarning
Error: Can't get attribute '_RemainderColsList'
```

## Input Validation

`src/common/validation.py` provides:

| Function | Used By | Checks |
|----------|---------|--------|
| `validate_uci_features()` | Models 1, 2 | All 32 feature columns present |
| `validate_risk_input()` | Model 3 | 5 fields present, numeric types, valid ranges |
| `to_feature_dataframe()` | Models 1, 2 | Validates + builds single-row DataFrame |

Validation failures raise `ValidationError` (subclass of `ValueError`).

### Model 3 Validation Rules

| Field | Rule |
|-------|------|
| absences | int/float, ≥ 0 |
| G1 | int/float, 0–20 |
| G2 | int/float, 0–20 |
| failures | int/float, ≥ 0 |
| studytime | int, 1–4 |

## Preprocessing

- **Models 1 & 2:** Preprocessing is inside the saved sklearn `Pipeline`. Callers provide raw feature dicts; the pipeline handles OneHotEncoding automatically.
- **Model 3:** No preprocessing. Fields are used directly for tier scoring.

## Response Format

See input/output contracts in:

- [model_1_performance.md](model_1_performance.md#18-output-contract)
- [model_2_pass_fail.md](model_2_pass_fail.md#16-output-contract)
- [model_3_risk_assessment.md](model_3_risk_assessment.md#10-output)

## Error Handling

| Error | Cause | Handling |
|-------|-------|----------|
| `ValidationError` | Missing or invalid input fields | Raise to caller; FastAPI should return 422 |
| `FileNotFoundError` | Model artifact missing | Raise to caller; FastAPI should return 503 |
| sklearn unpickle error | Version mismatch | Pin scikit-learn==1.6.1 |

## FastAPI Integration (Planned)

Backend stubs exist at `backend/app/ml/predictor.py` and `backend/app/ml/model_loader.py` (currently TODO).

Conceptual flow:

```
FastAPI Request
    ↓
Pydantic schema validation
    ↓
Call ml/src predictor function
    ↓
Return JSON response
```

### Suggested Endpoint Mapping

| Endpoint | Function | Input Schema |
|----------|----------|--------------|
| `POST /api/ml/performance` | `predict_performance()` | 32 UCI features |
| `POST /api/ml/pass-fail` | `predict_pass_fail()` | 32 UCI features |
| `POST /api/ml/risk` | `assess_student_risk()` | 5 risk fields |

### Integration Options

1. **Import directly:** Add `ml/src` to Python path and import predictor functions
2. **Package install:** Install `prj649-ml` as editable package via `uv pip install -e ml/`
3. **Copy artifacts:** Backend loads `.pkl` and `.json` from a configured path

The backend should not reimplement preprocessing — use the saved pipelines.

## Running Tests

```bash
cd ml
uv run pytest tests/ -v
```

Tests verify model loading, valid predictions, invalid input rejection, and risk level thresholds.
