import type {
  AtRiskSummary,
  AttendancePerformancePoint,
  ChartBucket,
  CourseAnalytics,
  DepartmentAnalytics,
  DepartmentRiskStack,
  InstitutionalAnalytics,
  PassFailTrendPoint,
  PerformanceIndicators,
  PerformanceTrendPoint,
  PredictionPassFailAnalytics,
  PredictionPerformanceAnalytics,
  PredictionRiskAnalytics,
  RiskDistribution,
  RiskFactorCount,
} from "@/types/analytics";

export interface ReportFilterLabels {
  academic_year: string;
  semester: string;
  department: string;
  program: string;
  course: string;
  risk_level: string;
}

export interface ReportHeader {
  institution_name: string;
  title: string;
  scope: string;
  generated_at: string;
  filters: ReportFilterLabels;
}

export interface ReportKPIs {
  overview: InstitutionalAnalytics;
  average_attendance: number;
  fail_percentage: number;
  average_predicted_marks: number;
  average_pass_probability: number;
  average_risk_score: number;
}

export interface AtRiskReportRow {
  student_id: string;
  student_name: string;
  roll_number: string;
  risk_score: number;
  risk_level: string;
  department_name?: string | null;
  program_name?: string | null;
  semester?: number | null;
  attendance_percentage?: number | null;
  cgpa?: number | null;
  backlog_count?: number | null;
  performance_trend?: string | null;
}

export interface ReportContext {
  header: ReportHeader;
  kpis: ReportKPIs;
  cgpa_distribution: ChartBucket[];
  sgpa_distribution: ChartBucket[];
  performance_trends: PerformanceTrendPoint[];
  course_performance: CourseAnalytics[];
  pass_fail_trend: PassFailTrendPoint[];
  attendance_distribution: ChartBucket[];
  attendance_performance: AttendancePerformancePoint[];
  performance_indicators: PerformanceIndicators;
  prediction_performance: PredictionPerformanceAnalytics;
  prediction_pass_fail: PredictionPassFailAnalytics;
  prediction_risk: PredictionRiskAnalytics;
  risk_distribution: RiskDistribution;
  risk_factors: RiskFactorCount[];
  department_analytics: DepartmentAnalytics[];
  department_risk_stacks: DepartmentRiskStack[];
  at_risk_students: AtRiskReportRow[];
  findings: string[];
}
