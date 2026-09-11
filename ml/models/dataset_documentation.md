# Dataset Documentation: Institutional Analytics & ML System

## 1. Generation Logic & Architecture
This synthetic dataset simulates a 4-cohort engineering university following standard Indian university academic frameworks (Choice Based Credit System - CBCS). Data generation employs a **latent trait simulation engine**, ensuring multi-variable dependencies (e.g., student ability drives study habits, which influence attendance, directly impacting Continuous Assessment (CA) and End-Term Exam scores).

## 2. File Schema & Data Types

### `student_master.csv`
- `student_id` (String): Synthetic unique identifier (`Student_000001`).
- `registration_number` (String): Unique academic registration number (`20231CSE0001`).
- `batch_year` (Integer): Cohort entry year (2023–2026).
- `branch_code` (String): Engineering discipline code (`CSE`, `ECE`, `ME`, etc.).
- `branch_name` (String): Full branch title.
- `section` (Char): Assigned class section (A–E).
- `gender` (Char): `M` / `F`.
- `age_at_admission` (Integer): Admission age (17–20).
- `admission_category` (String): Seat quota (`GENERAL`, `OBC`, `SC`, `ST`, `MANAGEMENT`, `SPORTS`).
- `entry_type` (String): `REGULAR` or `LATERAL_ENTRY`.

### `course_master.csv`
- `course_code` (String): Unique identifier (`CSE201`).
- `course_name` (String): Title of the course.
- `branch_code` (String): Associated department.
- `semester` (Integer): Semester offering (1–8).
- `course_type` (String): `THEORY`, `LAB`, `PROJECT`, `INTERNSHIP`, `NON_CREDIT`.
- `credits` (Integer): Course credit weight (1–6).
- `assessment_type` (String): Evaluation schema (`CA_MID_END`, `CA_END`, `PRACTICAL`, `PROJECT`).

### `assessment_marks.csv`
- `student_id` (String): Relational student ID.
- `course_code` (String): Relational course ID.
- `component` (String): Evaluation event (`CA`, `MID`, `END`, `PRACTICAL`, `PROJECT`).
- `marks` (Float): Obtained raw score.
- `max_marks` (Float): Total possible marks for the component.
- `percentage` (Float): Standardized percentage.

### `semester_results.csv`
- `student_id` / `course_code` / `semester` / `academic_year`.
- `CA`, `MID`, `END`, `PRACTICAL` (Float): Component scores (NaN if not applicable).
- `TOTAL_MARKS` (Float): Sum of earned marks.
- `PERCENTAGE` (Float): Aggregated score percentage.
- `GRADE` / `GRADE_POINT` (String/Integer): Letter grade and 10-point scale equivalent.
- `RESULT_STATUS` (String): `PASS` / `FAIL`.
- `ATTEMPT_TYPE` (String): `REGULAR`, `MAKEUP`, `SUMMER`.

### `student_semester_features.csv`
- Behavioral metrics per semester: `attendance_percentage`, `study_hours_per_week`, `assignments_completed_percentage`, `class_participation`.
- Dynamic academic indicators: `sgpa`, `cgpa`, `previous_sgpa`, `previous_cgpa`, `backlog_count`, `current_failed_courses`, `low_performance_course_count`, `performance_trend` (`IMPROVING`, `STABLE`, `DECLINING`).

## 3. Grading, SGPA, and CGPA Calculation

### Grading Scale
| Percentage Range | Grade | Grade Point | Outcome |
| :--- | :--- | :--- | :--- |
| $\ge 90\%$ | O | 10 | PASS |
| $80\% - 89\%$ | A+ | 9 | PASS |
| $70\% - 79\%$ | A | 8 | PASS |
| $60\% - 69\%$ | B+ | 7 | PASS |
| $55\% - 54\%$ | B | 6 | PASS |
| $50\% - 54\%$ | C | 5 | PASS |
| $40\% - 49\%$ | D | 4 | PASS |
| $< 40\%$ | F | 0 | FAIL |

### SGPA & CGPA Equations
SGPA is calculated per semester as the credit-weighted sum of grade points divided by total registered credits:
$$\text{SGPA} = \frac{\sum_{i=1}^{N} (\text{Credit}_i \times \text{GradePoint}_i)}{\sum_{i=1}^{N} \text{Credit}_i}$$

CGPA is computed cumulatively across all credit-bearing courses completed up to the current semester:
$$\text{CGPA} = \frac{\sum_{j=1}^{M} (\text{Credit}_j \times \text{GradePoint}_j)}{\sum_{j=1}^{M} \text{Credit}_j}$$

## 4. Backlog & Re-evaluation Logic
1. When a student earns an `F` grade in a `REGULAR` attempt, `backlog_count` increases by 1, and the course code enters `active_backlogs`.
2. Re-examinations (`MAKEUP` or `SUMMER`) are appended as new rows in `semester_results.csv`.
3. If the re-examination result is `PASS`, `backlog_count` decreases by 1 in subsequent semesters. Historical failed attempts remain preserved to maintain auditability.

## 5. Machine Learning Targets & Leakage Prevention Strategy

### Model 1: Continuous End-Term Mark Prediction (Regression)
- **Target**: `TARGET_END_MARKS` (Range: 0–100).
- **Features**: `CA_mark`, `MID_mark`, `attendance_percentage`, `study_hours_per_week`, `assignment_completion_pct`, `previous_sgpa`, `previous_cgpa`, `backlog_count`, `course_credits`, `course_type`, `branch`, `semester`.
- **Leakage Prevention**: Excludes current semester `END` marks, overall course `TOTAL_MARKS`, final `GRADE`, current `SGPA`, and current `CGPA`.

### Model 2: Course Pass/Fail Prediction (Binary Classification)
- **Target**: `TARGET_PASS_FAIL` (1 for PASS, 0 for FAIL).
- **Features**: Pre-examination features identical to Model 1. Excludes all post-examination metrics (`END` marks, overall grade, current SGPA/CGPA).

### Model 3: Student At-Risk Detection (Multi-class / Screening)
- **Target**: Raw behavioral and performance features provided directly (`attendance_percentage`, `CA_average`, `backlog_count`, `performance_trend`, etc.).
- **Independent Validation Label**: `INDEPENDENT_RISK_LABEL` (`LOW`, `MEDIUM`, `HIGH`) generated via a separate simulated retention/intervention model to prevent circular rule evaluation.
