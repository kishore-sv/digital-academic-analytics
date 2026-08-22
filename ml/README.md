# PRJ_649 ML Development

Machine learning development for academic performance prediction, at-risk detection, and pass/fail prediction.

## Setup

```bash
uv sync
```

## Structure

```
ml/
├── datasets/raw/        # Raw academic datasets
├── datasets/processed/  # Cleaned and processed data
├── notebooks/           # Jupyter notebooks for EDA and experimentation
├── src/                 # Training and evaluation scripts
└── models/              # Trained pickle models (not yet created)
```

## Planned Models

### 1. Performance Prediction
- **Inputs:** Attendance, internal marks, assignment marks, previous GPA/CGPA, previous semester marks, backlogs, academic history
- **Outputs:** Predicted final marks, predicted grade, performance category

### 2. At-Risk Student Detection
- **Inputs:** Attendance, internal marks, previous CGPA, backlogs, assignment performance, previous results
- **Outputs:** Low / Medium / High risk, risk probability

### 3. Pass/Fail Prediction
- **Inputs:** Attendance, internal marks, previous CGPA, assignment marks, backlogs, academic history
- **Outputs:** Pass / Fail, probability

## Note

Models have not been trained yet. This directory contains the structure and stubs for future development.
