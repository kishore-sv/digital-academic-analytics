# ML Pipeline

## Overview

The ML pipeline is developed separately in the `ml/` directory and integrated into the FastAPI backend for inference.

**Models have not been trained yet.** This document describes the planned pipeline and model specifications.

## Pipeline Stages

```
Dataset
    ↓
Data Cleaning
    ↓
EDA (Exploratory Data Analysis)
    ↓
Feature Engineering
    ↓
Training
    ↓
Evaluation
    ↓
Pickle Model (.pkl)
    ↓
FastAPI Inference (backend/app/ml/)
    ↓
Next.js Dashboard
```

## Planned Models

### 1. Student Performance Prediction

**Inputs:**
- Attendance
- Internal marks
- Assignment marks
- Previous GPA/CGPA
- Previous semester marks
- Backlogs
- Academic history

**Outputs:**
- Predicted final marks
- Predicted grade
- Performance category

**Output file:** `ml/models/performance_model.pkl`

### 2. At-Risk Student Detection

**Inputs:**
- Attendance
- Internal marks
- Previous CGPA
- Backlogs
- Assignment performance
- Previous results

**Outputs:**
- Low / Medium / High risk
- Risk probability

**Output file:** `ml/models/risk_model.pkl`

### 3. Pass/Fail Prediction

**Inputs:**
- Attendance
- Internal marks
- Previous CGPA
- Assignment marks
- Backlogs
- Academic history

**Outputs:**
- Pass / Fail
- Probability

**Output file:** `ml/models/pass_fail_model.pkl`

## Development Location

| Stage | Location |
|-------|----------|
| Raw data | `ml/datasets/raw/` |
| Processed data | `ml/datasets/processed/` |
| Notebooks | `ml/notebooks/` |
| Training scripts | `ml/src/` |
| Trained models | `ml/models/` |
| Inference | `backend/app/ml/` |

## Related Documentation

- [Architecture](architecture.md)
- [Development Phases](development-phases.md)
