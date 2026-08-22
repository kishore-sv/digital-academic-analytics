export interface PerformanceRecord {
  id: string;
  studentId: string;
  subjectId: string;
  subjectName: string;
  internalMarks: number;
  assignmentMarks: number;
  examMarks: number;
  grade: string;
  semester: number;
}

export interface PerformanceSummary {
  studentId: string;
  cgpa: number;
  totalCredits: number;
  backlogs: number;
  attendancePercentage: number;
}
