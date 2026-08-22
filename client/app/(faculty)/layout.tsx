"use client";

import { RoleShell } from "@/components/layout/role-shell";
import { facultyNavItems } from "@/components/layout/faculty-nav";
import { ROUTES } from "@/lib/constants";

export default function FacultyLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RoleShell
      navItems={facultyNavItems}
      roleLabel="Faculty"
      homeHref={ROUTES.faculty.dashboard}
    >
      {children}
    </RoleShell>
  );
}
