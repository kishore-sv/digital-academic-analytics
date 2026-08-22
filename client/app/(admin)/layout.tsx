"use client";

import { RoleShell } from "@/components/layout/role-shell";
import { adminNavItems } from "@/components/layout/admin-nav";
import { ROUTES } from "@/lib/constants";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RoleShell
      navItems={adminNavItems}
      roleLabel="Institution Admin"
      homeHref={ROUTES.admin.dashboard}
    >
      {children}
    </RoleShell>
  );
}
