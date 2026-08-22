"use client";

import { RoleShell } from "@/components/layout/role-shell";
import { studentNavItems } from "@/components/layout/student-nav";
import { ROUTES } from "@/lib/constants";

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RoleShell
      navItems={studentNavItems}
      roleLabel="Student"
      homeHref={ROUTES.student.dashboard}
    >
      {children}
    </RoleShell>
  );
}
