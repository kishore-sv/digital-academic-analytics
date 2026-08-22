import type { UserRole } from "@/types/auth";

export interface AuthState {
  userId: string | null;
  role: UserRole | null;
  institutionId: string | null;
  isAuthenticated: boolean;
}

export const INITIAL_AUTH_STATE: AuthState = {
  userId: null,
  role: null,
  institutionId: null,
  isAuthenticated: false,
};

// TODO: Implement authentication logic when backend is ready
