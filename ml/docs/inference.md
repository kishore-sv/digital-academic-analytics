# Inference

Python inference layer for FastAPI integration (integration not yet implemented in backend).

## Setup

```bash
cd ml
uv sync
```

## Model 1 — Performance

```python
from src.model_1.predictor import predict_performance

features = {
    "school": "GP", "sex": "F", "age": 18,
    # ... all 32 UCI feature columns
}
result = predict_performance(features)
# {"predicted_g3": 6.12}
```

## Model 2 — Pass/Fail

```python
from src.model_2.predictor import predict_pass_fail

result = predict_pass_fail(features)  # same 32 features as Model 1
# {
#   "prediction": "PASS",
#   "pass_probability": 0.85,
#   "fail_probability": 0.15
# }
```

## Model 3 — Risk Assessment

```python
from src.model_3.risk_engine import assess_student_risk

result = assess_student_risk({
    "absences": 6,
    "G1": 10,
    "G2": 9,
    "failures": 1,
    "studytime": 2,
})
```

## Artifact Paths

Resolved via `src/common/paths.py`:

| Artifact | Path |
|----------|------|
| Model 1 | `ml/models/model_1/performance_model.pkl` |
| Model 2 | `ml/models/model_2/pass_fail_model.pkl` |
| Model 3 config | `ml/models/model_3/risk_engine_config.json` |
| Dataset | `ml/data/raw/student-mat.csv` |

## Validation

`src/common/validation.py` enforces:
- Model 1/2: all 32 feature columns present
- Model 3: required fields with type and range checks (`G1`/`G2` 0–20, `studytime` 1–4, etc.)

Raises `ValidationError` on missing or invalid input.

## Loading Models

Models are lazy-loaded on first prediction via `joblib.load`. The sklearn `Pipeline` includes preprocessing — no separate transform step needed for Models 1 and 2.

## FastAPI Integration (planned)

Backend stub: `backend/app/ml/`. Will call these Python functions or load artifacts directly once integrated.

```python
# Planned flow:
# POST /api/v1/predictions/performance  → predict_performance()
# POST /api/v1/predictions/pass-fail      → predict_pass_fail()
# POST /api/v1/predictions/risk           → assess_student_risk()
```

## Tests

```bash
uv run pytest tests/
```
