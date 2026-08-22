export interface DepartmentAnalytics {
  departmentId: string;
  departmentName: string;
  studentCount: number;
  averageGpa: number;
  atRiskCount: number;
}

export interface SubjectAnalytics {
  subjectId: string;
  subjectName: string;
  averageMarks: number;
  passRate: number;
}

export interface InstitutionalAnalytics {
  totalStudents: number;
  totalFaculty: number;
  averageGpa: number;
  atRiskPercentage: number;
  departmentCount: number;
}
