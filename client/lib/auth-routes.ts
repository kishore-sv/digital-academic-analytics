import { ROUTES } from "@/lib/constants";
import type { UserRole } from "@/types/auth";

const ROLE_LABELS: Record<UserRole, string> = {
  institution_admin: "Institution Admin",
  student: "Student",
  faculty: "Faculty",
  parent: "Parent",
};

export function getProfileHref(role: UserRole): string {
  switch (role) {
    case "institution_admin":
      return ROUTES.admin.profile;
    case "student":
      return ROUTES.student.profile;
    case "faculty":
      return ROUTES.faculty.profile;
    case "parent":
      return ROUTES.parent.profile;
  }
}

export function getRoleLabel(role: UserRole): string {
  return ROLE_LABELS[role];
}

export function getUserDisplayName(
  user: { name?: string | null; email?: string | null },
): string {
  return user.name?.trim() || user.email?.trim() || "Account";
}
