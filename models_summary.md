# Student Academic Intelligence — ML Models Summary

This document summarizes the three academic intelligence components developed for the ERP system.

---

# Model 1 — Student Performance Prediction

## Purpose

Model 1 predicts a student's final academic performance.

### Question answered

> "What final grade is this student likely to achieve?"

## ML Problem

**Regression**

The model predicts the student's final grade (`G3`) as a numerical value.

```text
Academic Information
        ↓
Performance Model
        ↓
Predicted Final Grade (G3)
````

## Dataset

Source:

**UCI Student Performance Dataset**

Dataset used:

```text
student-mat.csv
```

Dataset size:

```text
395 students
33 columns
```

Target:

```text
G3
```

Input features:

```text
32 features
```

The input features include:

### Numerical

```text
age
Medu
Fedu
traveltime
studytime
failures
famrel
freetime
goout
Dalc
Walc
health
absences
G1
G2
```

### Categorical

```text
school
sex
address
famsize
Pstatus
Mjob
Fjob
reason
guardian
schoolsup
famsup
paid
activities
nursery
higher
internet
romantic
```

## Models Compared

Three regression algorithms were evaluated:

1. Linear Regression
2. Random Forest Regressor
3. HistGradientBoostingRegressor

## Model Comparison

| Model                |    MAE |   RMSE |     R² |
| -------------------- | -----: | -----: | -----: |
| HistGradientBoosting | 1.2321 | 1.9348 | 0.8174 |
| Random Forest        | 1.1863 | 2.0023 | 0.8045 |
| Linear Regression    | 1.6467 | 2.3784 | 0.7241 |

## Selected Model

```text
HistGradientBoostingRegressor
```

Final test performance:

```text
MAE  : 1.2321
RMSE : 1.9348
R²   : 0.8174
```

## Model Artifact

```text
performance_model.pkl
```

The saved artifact is a complete:

```text
sklearn.pipeline.Pipeline
```

containing preprocessing and the trained model.

## Example Output

```text
Predicted final grade (G3): 13.70
```

---

# Model 2 — Student Pass/Fail Prediction

## Purpose

Model 2 predicts whether a student is likely to pass or fail based on academic information.

### Question answered

> "Is this student likely to pass or fail?"

## ML Problem

**Binary Classification**

Classes:

```text
PASS
FAIL
```

Architecture:

```text
Academic Information
        ↓
Pass/Fail Classifier
        ↓
PASS / FAIL
        +
Pass Probability
        +
Fail Probability
```

## Dataset

Source:

**UCI Student Performance Dataset**

Dataset used:

```text
student-mat.csv
```

Dataset size:

```text
395 students
33 columns
```

The final grade `G3` was used to derive the PASS/FAIL target.

The model inputs exclude `G3`.

Input:

```text
32 features
```

Target:

```text
pass_fail
```

Target distribution:

```text
PASS : 265 (67.09%)
FAIL : 130 (32.91%)
```

## Models Compared

Three classification algorithms were evaluated:

1. Logistic Regression
2. Random Forest Classifier
3. HistGradientBoostingClassifier

## Model Comparison

| Model                | Accuracy | Precision (FAIL) | Recall (FAIL) | F1 (FAIL) | ROC-AUC |
| -------------------- | -------: | ---------------: | ------------: | --------: | ------: |
| Logistic Regression  |   0.8861 |           0.7742 |        0.9231 |    0.8421 |  0.9652 |
| Random Forest        |   0.8734 |           0.7500 |        0.9231 |    0.8276 |  0.9376 |
| HistGradientBoosting |   0.8734 |           0.7500 |        0.9231 |    0.8276 |  0.9565 |

## Selected Model

```text
Logistic Regression
```

Final test performance:

```text
Accuracy  : 0.8861
Precision : 0.7742
Recall    : 0.9231
F1 Score  : 0.8421
ROC-AUC   : 0.9652
```

### Important Metric

FAIL recall is particularly important for the ERP's early-warning use case.

```text
FAIL Recall = 92.31%
```

On the 79-student test set:

```text
Actual FAIL → Predicted FAIL : 24
Actual FAIL → Predicted PASS : 2

Actual PASS → Predicted FAIL : 7
Actual PASS → Predicted PASS : 46
```

Therefore, the model identified:

```text
24 / 26 actual FAIL students
```

in the test set.

## Model Artifact

```text
pass_fail_model.pkl
```

The saved artifact is a complete:

```text
sklearn.pipeline.Pipeline
```

containing preprocessing and the trained Logistic Regression model.

## Output

The model produces:

```text
Prediction: PASS / FAIL

Pass Probability: XX%
Fail Probability: XX%
```

Example:

```text
Prediction: PASS
Pass Probability: 99.99%
Fail Probability: 0.01%
```

### Important Note

The probability is the model's estimated probability, not a guaranteed real-world probability.

---

# Model 3 — Student At-Risk Detection

## Purpose

Model 3 identifies students who may require academic intervention.

### Question answered

> "Which students are currently at risk and may need attention?"

Unlike Models 1 and 2, Model 3 is currently **not an ML classifier**.

It is a transparent, rule-based **risk engine**.

```text
Academic Indicators
        ↓
Risk Engine
        ↓
Risk Score
        ↓
LOW / MEDIUM / HIGH
        +
Risk Indicators
```

## Why a Rule-Based Engine?

The UCI dataset does not contain a reliable historical target such as:

```text
AT_RISK
NOT_AT_RISK
```

or actual intervention outcomes.

Therefore, training an ML classifier would require inventing labels.

That would make the model learn an arbitrary rule rather than learn from genuine historical intervention data.

For the current project, a transparent risk engine is more appropriate.

## Current Inputs

The risk engine uses:

```text
absences
G1
G2
failures
studytime
```

It intentionally does **not** use:

```text
G3
```

because `G3` is the final grade and would introduce future/outcome information into an early-risk assessment.

## Risk Components

### 1. Absence Risk

```text
0–4 absences  → LOW
5–9            → MEDIUM
10+            → HIGH
```

Weight:

```text
25%
```

### 2. Current Performance Risk

Based on `G2`:

```text
G2 >= 12 → LOW
G2 10–11 → MEDIUM
G2 < 10  → HIGH
```

Weight:

```text
30%
```

### 3. Performance Trend Risk

Performance trend:

```text
G2 - G1
```

Classification:

```text
Improving → LOW
Stable    → MEDIUM
Declining → HIGH
```

Weight:

```text
20%
```

### 4. Previous Failure Risk

Based on `failures`:

```text
0 failures → LOW
1 failure  → MEDIUM
2+         → HIGH
```

Weight:

```text
15%
```

### 5. Study-Time Risk

Based on `studytime`:

```text
3–4 → LOW
2   → MEDIUM
1   → HIGH
```

Weight:

```text
10%
```

## Risk Score

The weighted components produce a score between:

```text
0–100
```

Formula:

```text
Risk Score =

Absence Risk       × 25%
Performance Risk   × 30%
Trend Risk         × 20%
Failure Risk       × 15%
Study-Time Risk    × 10%
```

Each component is normalized from:

```text
0 = LOW
1 = MEDIUM
2 = HIGH
```

before applying its weight.

## Risk Levels

```text
0–30   → LOW
31–60  → MEDIUM
61–100 → HIGH
```

## Dataset Validation

The engine was executed against all:

```text
395 students
```

Result:

```text
LOW       : 165 (41.77%)
MEDIUM    : 151 (38.23%)
HIGH      : 79  (20.00%)
```

Risk score statistics:

```text
Mean   : 39.49
Median : 35.00
Min    : 0
Max    : 100
```

## Actionable Risk Indicators

The engine can identify specific areas requiring attention.

Examples:

```text
High Absence
Moderate Absence

Low Current Performance
Moderate Current Performance

Declining Performance
Stable Performance

Multiple Previous Failures
Previous Failure

Low Study Time
Moderate Study Time
```

Example:

```text
Risk Score : 100/100
Risk Level : HIGH

Indicators:
- High Absence
- Low Current Performance
- Declining Performance
- Multiple Previous Failures
- Low Study Time
```

## Leakage Validation

The risk engine was explicitly tested to ensure that changing `G3` does not change the risk result.

Result:

```text
Risk results identical: True
```

Therefore, the current risk engine does not depend on the final grade.

## Model Artifact

Model 3 does not currently use a `.pkl` file.

Configuration is stored in:

```text
risk_engine_config.json
```

The configuration contains:

```text
weights
thresholds
risk-level boundaries
component boundaries
```

The configuration was saved and reloaded successfully.

---

# Overall Three-Component Architecture

The three components serve different purposes.

```text
                    STUDENT DATA
                         │
             ┌───────────┼───────────┐
             │           │           │
             ↓           ↓           ↓
        MODEL 1      MODEL 2      MODEL 3
       Performance   Pass/Fail    Risk Engine
             │           │           │
             ↓           ↓           ↓
       Predicted G3   Probability  Risk Score
                                   + Level
             │           │           │
             └───────────┼───────────┘
                         ↓
                  ACADEMIC INSIGHTS
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Student         Faculty        Admin
```

## Component Summary

| Component | Type                   | Primary Output                            | Artifact                  |
| --------- | ---------------------- | ----------------------------------------- | ------------------------- |
| Model 1   | Regression             | Predicted G3                              | `performance_model.pkl`   |
| Model 2   | Binary Classification  | PASS/FAIL + probabilities                 | `pass_fail_model.pkl`     |
| Model 3   | Rule-Based Risk Engine | Risk score + LOW/MEDIUM/HIGH + indicators | `risk_engine_config.json` |

---

# Important Limitations

## Dataset Size

The models were developed using:

```text
395 students
```

This is relatively small for a production academic prediction system.

Therefore, the reported test metrics should **not** be interpreted as guaranteed real-world performance.

## Dataset Domain

The UCI dataset represents student performance in a specific educational context.

The features do not directly correspond to all ERP fields such as:

```text
Attendance %
Internal Marks
Assignment Scores
Previous CGPA
Current Semester CGPA
Department
Course-wise performance
```

These should be mapped or retrained using actual ERP data when available.

## Model 3

The Model 3 weights and thresholds are:

```text
system-defined heuristic values
```

They are not scientifically validated probabilities.

They should eventually be tuned or replaced using historical institutional data and academic expert feedback.

## Future Improvement

When the ERP accumulates historical academic/intervention data, Model 3 can potentially become a genuine ML classifier:

```text
Historical Academic Data
          ↓
Actual Intervention Outcome
          ↓
AT_RISK / NOT_AT_RISK
          ↓
ML Classification Model
          ↓
Validated Risk Prediction
```

---

# Current Project Status

```text
Model 1
[COMPLETED]
performance_model.pkl

Model 2
[COMPLETED]
pass_fail_model.pkl

Model 3
[COMPLETED - RULE ENGINE]
risk_engine_config.json

FastAPI Integration
[NOT YET IMPLEMENTED]
```

The three components are currently developed and validated independently in Google Colab notebooks:

```text
performance_model.ipynb
pass_fail_model.ipynb
risk_model.ipynb
```

