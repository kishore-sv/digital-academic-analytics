"use client";

import { RoleShell } from "@/components/layout/role-shell";
import { parentNavItems } from "@/components/layout/parent-nav";
import { ROUTES } from "@/lib/constants";

export default function ParentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <RoleShell
      navItems={parentNavItems}
      roleLabel="Parent"
      homeHref={ROUTES.parent.dashboard}
    >
      {children}
    </RoleShell>
  );
}
