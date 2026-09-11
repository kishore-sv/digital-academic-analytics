import type { UserRole } from "@/types/auth";

const SESSION_ROLE_COOKIE = "session_role";
const MAX_AGE_SECONDS = 7 * 24 * 60 * 60;

export function setSessionRole(role: UserRole) {
  if (typeof document === "undefined") return;
  document.cookie = `${SESSION_ROLE_COOKIE}=${role}; path=/; max-age=${MAX_AGE_SECONDS}; samesite=lax`;
}

export function clearSessionRole() {
  if (typeof document === "undefined") return;
  document.cookie = `${SESSION_ROLE_COOKIE}=; path=/; max-age=0; samesite=lax`;
}

export const ROLE_DASHBOARD: Record<string, string> = {
  institution_admin: "/admin/dashboard",
  student: "/student/dashboard",
  faculty: "/faculty/dashboard",
  parent: "/parent/dashboard",
};
