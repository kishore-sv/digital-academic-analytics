/**
 * ML pipeline labels aligned with `backend/app/services/feature_preparation.py`,
 * `prediction_service.py`, and `ml/risk_engine.py`.
 */

export const FEATURE_PREPARATION_FIELDS = [
  { key: "CA_mark", label: "CA marks", source: "AssessmentMark (CA)" },
  { key: "MID_mark", label: "Mid-term marks", source: "AssessmentMark (MID)" },
  { key: "attendance_percentage", label: "Attendance %", source: "Enrollment" },
  { key: "study_hours_per_week", label: "Study hours / week", source: "Enrollment" },
  { key: "assignment_completion_pct", label: "Assignment completion %", source: "Enrollment" },
  { key: "previous_sgpa", label: "Previous SGPA", source: "SemesterResult" },
  { key: "previous_cgpa", label: "Previous CGPA", source: "SemesterResult" },
  { key: "backlog_count", label: "Backlog count", source: "SemesterResult" },
  { key: "course_credits", label: "Course credits", source: "Course" },
  { key: "course_type", label: "Course type", source: "Course" },
  { key: "branch", label: "Branch", source: "Student" },
  { key: "semester", label: "Semester", source: "Student" },
  { key: "current_failed_courses", label: "Current failed courses", source: "SemesterResult" },
  { key: "low_performance_course_count", label: "Low performance course count", source: "SemesterResult" },
  { key: "performance_trend", label: "Performance trend", source: "SemesterResult" },
] as const;

export const ML_MODELS = [
  {
    id: "model1",
    name: "Model 1 — Performance prediction",
    implementation: "ML (joblib)",
    module: "app.ml.model1",
    outputs: ["predicted_end_marks"],
  },
  {
    id: "model2",
    name: "Model 2 — Pass / fail prediction",
    implementation: "ML (joblib)",
    module: "app.ml.model2",
    outputs: ["pass_fail_prediction", "pass_probability", "fail_probability"],
  },
  {
    id: "model3",
    name: "Model 3 — At-risk detection",
    implementation: "Rule-based weighted risk engine (not ML)",
    module: "app.ml.risk_engine",
    outputs: ["risk_score", "risk_level (LOW / MEDIUM / HIGH)", "risk_factors", "recommendations"],
  },
] as const;

export const RISK_ENGINE_FEATURES = [
  "attendance_percentage",
  "previous_cgpa",
  "backlog_count",
  "current_failed_courses",
  "low_performance_course_count",
  "study_hours_per_week",
  "assignment_completion_percentage",
  "performance_trend",
] as const;
