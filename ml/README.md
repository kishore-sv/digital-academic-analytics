# ML Module

Project: **PRJ_649** — Digital Academic Performance Monitoring and Institutional Analytics System

## Models

### Model 1 — Student Performance Prediction

- **Type:** Regression
- **Algorithm:** `HistGradientBoostingRegressor` (sklearn `Pipeline`)
- **Artifact:** `models/model_1/performance_model.pkl`
- **Output:** Predicted final grade (`G3`)

### Model 2 — Student Pass/Fail Prediction

- **Type:** Binary classification
- **Algorithm:** `LogisticRegression` (sklearn `Pipeline`)
- **Artifact:** `models/model_2/pass_fail_model.pkl`
- **Output:** `PASS` / `FAIL` with probabilities

### Model 3 — Student At-Risk Detection / Risk Assessment

- **Type:** Rule-based weighted scoring engine (not ML)
- **Configuration:** `models/model_3/risk_engine_config.json`
- **Output:** Risk score (0–100), risk level, indicators

## Purpose

This folder contains training notebooks, trained model artifacts, inference code, and documentation for the three academic intelligence components. It is designed for integration with the FastAPI backend.

**Authoritative documentation:** [`ml/docs/`](docs/README.md). Root-level `docs/ml-pipeline.md` describes an earlier planned pipeline and may not match this implementation.

## Setup

```bash
cd ml
uv sync
```

**Important:** Model 1 and Model 2 `.pkl` files were trained with **scikit-learn 1.6.1**. The project pins this version in `pyproject.toml`. Loading with a different sklearn version may fail.

## Folder Structure

```
ml/
├── README.md
├── requirements.txt
├── pyproject.toml
├── docs/                 # Model and pipeline documentation
├── notebooks/
│   ├── model_1/performance_model.ipynb
│   ├── model_2/pass_fail_model.ipynb
│   └── model_3/risk_model.ipynb
├── models/
│   ├── model_1/performance_model.pkl
│   ├── model_2/pass_fail_model.pkl
│   └── model_3/risk_engine_config.json
├── src/                  # Inference code
├── data/raw/             # UCI student-mat.csv
└── tests/
```

## Dataset

Training uses the **UCI Student Performance Dataset** (Mathematics course):

- Local path: `data/raw/student-mat.csv`
- Notebooks were developed in Google Colab with uploaded zip files; for local runs use the path above.

See [`data/README.md`](data/README.md) for column details.

## Inference

```python
from src.model_1.predictor import predict_performance
from src.model_2.predictor import predict_pass_fail
from src.model_3.risk_engine import assess_student_risk

# Model 1 — 32 UCI features (see src/common/features.py)
result = predict_performance(student_dict)
# {"predicted_g3": 13.7}

# Model 2 — same 32 features
result = predict_pass_fail(student_dict)
# {"prediction": "PASS", "pass_probability": 0.99, "fail_probability": 0.01}

# Model 3 — 5 risk fields
result = assess_student_risk({
    "absences": 6, "G1": 10, "G2": 9, "failures": 1, "studytime": 2
})
# {"risk_score": 47.5, "risk_level": "MEDIUM", "risk_indicators": [...], ...}
```

See [`docs/inference.md`](docs/inference.md) for input/output contracts and backend integration notes.

## Tests

```bash
uv run pytest tests/ -v
```

## Documentation

| Document | Description |
|----------|-------------|
| [docs/ml_architecture.md](docs/ml_architecture.md) | Architecture overview |
| [docs/models_overview.md](docs/models_overview.md) | Component comparison |
| [docs/model_1_performance.md](docs/model_1_performance.md) | Model 1 details |
| [docs/model_2_pass_fail.md](docs/model_2_pass_fail.md) | Model 2 details |
| [docs/model_3_risk_assessment.md](docs/model_3_risk_assessment.md) | Model 3 risk engine |
| [docs/data_pipeline.md](docs/data_pipeline.md) | Data loading and preprocessing |
| [docs/model_evaluation.md](docs/model_evaluation.md) | Evaluation metrics |
| [docs/inference.md](docs/inference.md) | Inference API |
