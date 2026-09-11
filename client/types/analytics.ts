export interface InstitutionalAnalytics {
  total_students: number;
  total_faculty: number;
  total_departments: number;
  average_cgpa: number;
  average_sgpa: number;
  pass_percentage: number;
  at_risk_percentage: number;
  high_risk_count: number;
}

export interface DepartmentAnalytics {
  department_id: string;
  department_name: string;
  average_cgpa: number;
  pass_percentage: number;
  student_count: number;
}

export interface CourseAnalytics {
  course_id: string;
  course_name: string;
  average_marks: number;
  pass_percentage: number;
}

export interface RiskDistribution {
  low: number;
  medium: number;
  high: number;
}

export interface ChartBucket {
  label: string;
  value: number;
}

export interface PerformanceTrendPoint {
  semester: string;
  average_sgpa: number | null;
  average_cgpa: number | null;
  pass_percentage: number | null;
}

export interface PassFailTrendPoint {
  semester: string;
  pass_count: number;
  fail_count: number;
}

export interface AttendancePerformancePoint {
  attendance_percentage: number;
  performance_value: number;
}

export interface PerformanceIndicators {
  improving: number;
  stable: number;
  declining: number;
}

export interface DepartmentRiskStack {
  department_id: string;
  department_name: string;
  low: number;
  medium: number;
  high: number;
}

export interface RiskFactorCount {
  factor: string;
  count: number;
}

export interface PredictionPerformanceAnalytics {
  average_predicted_marks: number;
  distribution: ChartBucket[];
  department_averages: ChartBucket[];
}

export interface PredictionPassFailAnalytics {
  predicted_pass_count: number;
  predicted_fail_count: number;
  average_pass_probability: number;
  probability_distribution: ChartBucket[];
  department_pass_rates: ChartBucket[];
}

export interface PredictionRiskAnalytics {
  average_risk_score: number;
  risk_distribution: RiskDistribution;
  department_stacks: DepartmentRiskStack[];
  score_distribution: ChartBucket[];
}

export interface AtRiskSummary {
  low: number;
  medium: number;
  high: number;
  risk_distribution: RiskDistribution;
  department_stacks: DepartmentRiskStack[];
  risk_factors: RiskFactorCount[];
}

export interface AnalyticsFilters {
  academic_year_id?: string;
  semester_id?: string;
  department_id?: string;
  program_id?: string;
  course_id?: string;
  risk_level?: string;
}

export function filtersToQuery(filters: AnalyticsFilters): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}
