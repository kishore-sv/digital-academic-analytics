export interface Student {
  id: string;
  rollNumber: string;
  name: string;
  email?: string;
  departmentId: string;
  program: string;
  semester: number;
  isLoginEnabled: boolean;
}

export interface StudentSummary {
  id: string;
  rollNumber: string;
  name: string;
  department: string;
  semester: number;
}
