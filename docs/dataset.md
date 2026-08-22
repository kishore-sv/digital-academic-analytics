# Dataset Strategy

## Overview

`ml/datasets/raw/` is currently **empty**. Without a dataset, all downstream work is blocked:

- ML model training (Phases 3–4)
- Analytics dashboard development (Phase 6)
- Backend seed data for local development
- End-to-end testing with realistic data

**Generating a synthetic dataset is the first implementation task**, not additional documentation.

## v1: Synthetic Dataset (required for Phase 1)

A Python script generates realistic fake academic data for local development and model training.

### Generator Script (planned)

```
ml/src/generate_synthetic.py
```

Run with:
```bash
cd ml && uv run python src/generate_synthetic.py
```

Output:
```
ml/datasets/raw/synthetic_academic_data.csv
```

### Dataset Scope

| Dimension | Value |
|-----------|-------|
| Institutions | 2 (Tenant A, Tenant B) |
| Departments per institution | 3 (CSE, ECE, MECH) |
| Students per institution | ~200 |
| Subjects per department | 5–8 |
| Semesters of history | 4 |
| Total rows (approx.) | ~3,200 student-semester records |

### Column Schema

| Column | Type | Description |
|--------|------|-------------|
| `institution_id` | string | `INST_A` or `INST_B` |
| `student_id` | string | Unique student identifier |
| `roll_number` | string | e.g. `20231CSE0260` |
| `department` | string | CSE, ECE, MECH |
| `semester` | int | 1–8 |
| `subject` | string | Subject name |
| `attendance_percentage` | float | 0–100 |
| `internal_marks` | float | 0–40 |
| `assignment_marks` | float | 0–20 |
| `exam_marks` | float | 0–100 (nullable for current semester) |
| `cgpa` | float | 0–10 |
| `backlogs` | int | 0–5 |
| `is_at_risk` | bool | Label for risk model |
| `passed` | bool | Label for pass/fail model |
| `performance_category` | string | `excellent`, `good`, `average`, `poor` |

### Label Generation Rules

Labels are derived from features using realistic rules (not random):

- **At-risk:** `attendance_percentage < 65` OR `cgpa < 5.0` OR `backlogs >= 2`
- **Pass/fail:** `passed = False` if `exam_marks < 40` OR `(internal_marks + assignment_marks) < 15`
- **Performance category:** Based on total marks percentage thresholds

This ensures the ML models have learnable patterns rather than random noise.

## v2: Real Anonymized Data (optional)

If real institutional data becomes available:
- Place in `ml/datasets/raw/institutional_data.csv`
- Anonymize: remove names, hash roll numbers, remove institution identifiers
- Document the anonymization process
- Never commit identifiable student data to version control

## Processed Dataset

After EDA and cleaning (Phase 2), processed data goes to:

```
ml/datasets/processed/
├── train.csv       # 80% stratified split
├── test.csv        # 20% stratified split
└── feature_matrix.pkl  # Engineered features for model training
```

## Seed Data for Backend (planned)

The synthetic dataset also feeds the backend seed script (Phase 5):

```
backend/scripts/seed.py   # loads synthetic_academic_data.csv into PostgreSQL
```

This provides realistic local dev data for:
- Testing analytics dashboards
- Verifying tenant isolation (INST_A data invisible to INST_B)
- Demo preparation

## Related Documentation

- [ML Pipeline](ml-pipeline.md)
- [ML Evaluation](ml-evaluation.md)
- [Development Phases](development-phases.md)
- [Database Design](database.md)
