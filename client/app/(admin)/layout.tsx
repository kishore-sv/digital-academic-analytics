"use client";

import { RoleShell } from "@/components/layout/role-shell";
import { adminSidebarNav } from "@/components/layout/admin-nav";
import { ROUTES } from "@/lib/constants";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RoleShell
      navConfig={adminSidebarNav}
      roleLabel="Institution Admin"
      homeHref={ROUTES.admin.dashboard}
      hideFooterProfile
    >
      {children}
    </RoleShell>
  );
}
