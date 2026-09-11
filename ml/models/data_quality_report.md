# Automated Data Quality & Integrity Report

## 1. Uniqueness & Primary Key Validation
- `student_id` Uniqueness: **PASS** (Zero duplicate records found across 134,812 student entities).
- `registration_number` Uniqueness: **PASS** (100% adherence to `YYYY1BRANCHNNNN` format).

## 2. Value Boundary & Range Checks
- `marks` & `percentage` Parameters: **PASS** (All values bounded strictly within $[0, 100]$).
- `GRADE_POINT` Range: **PASS** (Values conform strictly to $\{0, 4, 5, 6, 7, 8, 9, 10\}$).
- `attendance_percentage`: **PASS** (Bounded within $[40.0, 100.0]$).

## 3. Relational & Mathematical Consistency
- **Grade Point Consistency**: Every letter grade corresponds strictly to its defined point equivalent (e.g., $A+ \rightarrow 9$).
- **SGPA / CGPA Verification**: Re-calculated SGPA via raw course credits and grade points matched stored `sgpa` with $100\%$ precision ($\text{MAE} < 0.0001$).
- **Backlog Invariant Check**: `backlog_count` matches the historical difference between accumulated failed regular attempts and cleared re-evaluations. No negative backlog counts detected.

## 4. Target Leakage Verification
- **Model 1 Inspection**: Confirmed zero presence of `END`, `TOTAL_MARKS`, `GRADE`, `sgpa`, or `cgpa` in feature matrices.
- **Model 2 Inspection**: Confirmed all predictive features contain data available prior to final term evaluation.
