export type UserRole = "admin" | "student" | "faculty" | "parent";

export interface AuthUser {
  id: string;
  role: UserRole;
  institutionId: string;
  name: string;
  email?: string;
  rollNumber?: string;
}

export interface LoginCredentials {
  role: UserRole;
  identifier: string;
  password: string;
}

export interface SignupCredentials {
  name: string;
  email: string;
  password: string;
  institutionName: string;
}
