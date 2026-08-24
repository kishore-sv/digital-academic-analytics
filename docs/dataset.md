# Dataset Strategy

## Overview

The ML models are trained on the **UCI Student Performance Dataset**, committed at `ml/data/raw/student-mat.csv`.

| Property | Value |
|----------|-------|
| Source | [UCI Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance) |
| File | `student-mat.csv` (mathematics course) |
| Rows | 395 students |
| Columns | 33 |
| Separator | `;` |
| Missing values | None |

Attribute documentation: `ml/data/raw/student.txt`

## Columns

### Target and Derived Labels

| Column | Role |
|--------|------|
| `G3` | Final grade (0–20) — target for Model 1 |
| `pass_fail` | Derived: PASS if G3 ≥ 10 — target for Model 2 |

### Input Features (32)

All columns except `G3` are used as features for Models 1 and 2.

**Numerical (15):** `age`, `Medu`, `Fedu`, `traveltime`, `studytime`, `failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health`, `absences`, `G1`, `G2`

**Categorical (17):** `school`, `sex`, `address`, `famsize`, `Pstatus`, `Mjob`, `Fjob`, `reason`, `guardian`, `schoolsup`, `famsup`, `paid`, `activities`, `nursery`, `higher`, `internet`, `romantic`

### Model 3 Inputs

Model 3 uses only: `absences`, `G1`, `G2`, `failures`, `studytime`

## Unused Data

`student-por.csv` (Portuguese language course) is available from UCI but not used by any notebook.

## ERP Field Mapping (Future)

The UCI dataset does not include ERP-specific fields:

| ERP Field | UCI Equivalent (approximate) |
|-----------|---------------------------|
| Attendance % | `absences` (inverse relationship) |
| Internal marks | `G1`, `G2` |
| Final grade | `G3` |
| CGPA | Not available |
| Department/course | Not available |

When institutional data becomes available, models should be retrained on mapped ERP features.

## Processed Data

`ml/data/processed/` is reserved for future train/test exports. Training currently happens in notebooks with in-memory splits.

## Backend Seed Data (Future)

A separate synthetic seed dataset for PostgreSQL local development is planned for Phase 5. The UCI dataset is used for ML training only.

## Related Documentation

- [ML Pipeline](ml-pipeline.md)
- [ML Evaluation](ml-evaluation.md)
- [ML Data README](../ml/data/README.md)
- [Data Pipeline (ml/)](../ml/docs/data_pipeline.md)
