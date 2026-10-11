"use client";

import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import {
  AppSidebar,
  type NavItem,
  type SidebarNavConfig,
} from "@/components/app-sidebar";
import { PortalUserMenu } from "@/components/layout/portal-user-menu";

interface RoleShellProps {
  children: React.ReactNode;
  navItems?: NavItem[];
  navConfig?: SidebarNavConfig;
  roleLabel: string;
  homeHref: string;
  hideFooterProfile?: boolean;
}

export function RoleShell({
  children,
  navItems,
  navConfig,
  roleLabel,
  homeHref,
  hideFooterProfile,
}: RoleShellProps) {
  return (
    <SidebarProvider>
      <AppSidebar
        navItems={navItems}
        navConfig={navConfig}
        roleLabel={roleLabel}
        homeHref={homeHref}
        hideFooterProfile={hideFooterProfile}
      />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <PortalUserMenu />
        </header>
        <main className="flex flex-1 flex-col gap-4 p-4">{children}</main>
      </SidebarInset>
    </SidebarProvider>
  );
}
