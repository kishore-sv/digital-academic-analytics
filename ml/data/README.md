# Dataset

## Name

UCI Student Performance Dataset — Mathematics course (`student-mat.csv`)

## Source

UCI Machine Learning Repository — Student Performance Data Set.

Attribute descriptions are in `raw/student.txt`.

## Expected Location

```
ml/data/raw/student-mat.csv
ml/data/raw/student.txt
```

## Format

- **Separator:** `;` (semicolon)
- **Rows:** 395 students
- **Columns:** 33

## Loading

```python
import pandas as pd
df = pd.read_csv("data/raw/student-mat.csv", sep=";")
```

Notebooks in `notebooks/model_{1,2,3}/` were developed in Google Colab with uploaded zip archives (`student_data/student-mat.csv`). For local reproduction, use the path above.

## Columns

| Column | Type | Description |
|--------|------|-------------|
| school | categorical | GP or MS |
| sex | categorical | F or M |
| age | numeric | 15–22 |
| address | categorical | U (urban) or R (rural) |
| famsize | categorical | LE3 or GT3 |
| Pstatus | categorical | T or A |
| Medu | numeric | Mother's education (0–4) |
| Fedu | numeric | Father's education (0–4) |
| Mjob | categorical | Mother's job |
| Fjob | categorical | Father's job |
| reason | categorical | Reason to choose school |
| guardian | categorical | Student's guardian |
| traveltime | numeric | Home to school travel time (1–4) |
| studytime | numeric | Weekly study time (1–4) |
| failures | numeric | Number of past class failures |
| schoolsup | categorical | Extra educational support |
| famsup | categorical | Family educational support |
| paid | categorical | Extra paid classes |
| activities | categorical | Extra-curricular activities |
| nursery | categorical | Attended nursery school |
| higher | categorical | Wants higher education |
| internet | categorical | Internet access at home |
| romantic | categorical | In a romantic relationship |
| famrel | numeric | Family relationship quality (1–5) |
| freetime | numeric | Free time after school (1–5) |
| goout | numeric | Going out with friends (1–5) |
| Dalc | numeric | Workday alcohol consumption (1–5) |
| Walc | numeric | Weekend alcohol consumption (1–5) |
| health | numeric | Current health status (1–5) |
| absences | numeric | Number of school absences |
| G1 | numeric | First period grade (0–20) |
| G2 | numeric | Second period grade (0–20) |
| G3 | numeric | Final grade (0–20) — target for Model 1 |

## Required Columns by Model

### Model 1 (Performance Prediction)

- **Input:** All 32 columns except `G3`
- **Target (training only):** `G3`

### Model 2 (Pass/Fail Prediction)

- **Input:** All 32 columns except `G3` and `pass_fail` (derived target)
- **Target (training only):** `pass_fail` — `PASS` if G3 ≥ 10, else `FAIL`

### Model 3 (Risk Assessment)

- **Input:** `absences`, `G1`, `G2`, `failures`, `studytime`
- **Not used:** `G3` (excluded to avoid outcome leakage)

## Preprocessing

No explicit data cleaning is performed in the notebooks (0 missing values in the dataset). Preprocessing for Models 1 and 2 is embedded in the saved sklearn `Pipeline` artifacts:

- Numeric features: passthrough
- Categorical features: `OneHotEncoder(handle_unknown="ignore")`

Model 3 uses no dataset preprocessing — scoring is applied directly to the five input fields.
