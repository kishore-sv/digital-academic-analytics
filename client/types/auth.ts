export type UserRole =
  | "institution_admin"
  | "student"
  | "faculty"
  | "parent";

export interface AuthUser {
  id: string;
  email: string | null;
  role: UserRole;
  institution_id: string;
  name?: string | null;
}

export interface LoginCredentials {
  identifier: string;
  password: string;
  role: UserRole;
}

export interface SignupCredentials {
  name: string;
  email: string;
  password: string;
  institution_name: string;
}
