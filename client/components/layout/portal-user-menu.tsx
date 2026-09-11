"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { IconLogout, IconUser } from "@tabler/icons-react";
import { Button } from "@/components/ui/button";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useAuth } from "@/hooks/use-auth";
import { getProfileHref, getUserDisplayName } from "@/lib/auth-routes";

interface PortalUserMenuProps {
  variant?: "header" | "sidebar";
}

export function PortalUserMenu({ variant = "header" }: PortalUserMenuProps) {
  const pathname = usePathname();
  const { user, logout, isLoading } = useAuth();

  if (isLoading || !user) {
    return null;
  }

  const profileHref = getProfileHref(user.role);
  const displayName = getUserDisplayName(user);

  if (variant === "sidebar") {
    return (
      <SidebarMenu>
        <SidebarMenuItem>
          <SidebarMenuButton
            tooltip="Profile"
            isActive={pathname === profileHref}
            render={<Link href={profileHref} />}
          >
            <IconUser />
            <span>Profile</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
        <SidebarMenuItem>
          <SidebarMenuButton
            tooltip="Logout"
            onClick={() => logout()}
            className="text-destructive hover:text-destructive"
          >
            <IconLogout />
            <span>Logout</span>
          </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    );
  }

  return (
    <div className="ml-auto flex items-center gap-2">
      <span className="hidden text-sm text-muted-foreground sm:inline">
        {displayName}
      </span>
      <Button variant="outline" size="sm" render={<Link href={profileHref} />}>
        <IconUser className="size-4" />
        Profile
      </Button>
      <Button variant="ghost" size="sm" onClick={() => logout()}>
        <IconLogout className="size-4" />
        Logout
      </Button>
    </div>
  );
}
