"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useMemo, useState, type ComponentType } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { IconChevronRight, IconInnerShadowTop } from "@tabler/icons-react";
import { PortalUserMenu } from "@/components/layout/portal-user-menu";
import { BRAND } from "@/lib/brand";
import { cn } from "@/lib/utils";

export interface NavItem {
  title: string;
  href: string;
  icon: ComponentType<{ className?: string }>;
}

export interface NavGroup {
  title: string;
  icon: ComponentType<{ className?: string }>;
  items: NavItem[];
  /** Open when no child route is active (admin default). */
  defaultOpen?: boolean;
}

export interface SidebarNavConfig {
  standalone: NavItem[];
  groups: NavGroup[];
}

interface AppSidebarProps {
  navItems?: NavItem[];
  navConfig?: SidebarNavConfig;
  roleLabel: string;
  homeHref: string;
  /** Hide profile link in footer when it appears in the main nav. */
  hideFooterProfile?: boolean;
}

export function isNavItemActive(pathname: string, href: string) {
  if (pathname === href) return true;
  if (href.endsWith("/dashboard")) return false;
  return pathname.startsWith(`${href}/`);
}

function groupHasActiveChild(pathname: string, group: NavGroup) {
  return group.items.some((item) => isNavItemActive(pathname, item.href));
}

function buildInitialOpenState(
  pathname: string,
  groups: NavGroup[],
): Record<string, boolean> {
  const state: Record<string, boolean> = {};
  let anyActive = false;
  for (const group of groups) {
    const active = groupHasActiveChild(pathname, group);
    if (active) anyActive = true;
    state[group.title] = active;
  }
  if (!anyActive) {
    for (const group of groups) {
      if (group.defaultOpen) {
        state[group.title] = true;
      }
    }
  }
  return state;
}

export function AppSidebar({
  navItems,
  navConfig,
  roleLabel,
  homeHref,
  hideFooterProfile = false,
}: AppSidebarProps) {
  const pathname = usePathname();
  const groups = navConfig?.groups ?? [];
  const standalone = navConfig?.standalone ?? [];

  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>(() =>
    navConfig ? buildInitialOpenState(pathname, groups) : {},
  );

  useEffect(() => {
    if (!navConfig) return;
    setOpenGroups((prev) => {
      const next = { ...prev };
      for (const group of groups) {
        if (groupHasActiveChild(pathname, group)) {
          next[group.title] = true;
        }
      }
      return next;
    });
  }, [pathname, navConfig, groups]);

  const flatItems = useMemo(() => navItems ?? [], [navItems]);

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" render={<Link href={homeHref} />}>
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                <IconInnerShadowTop className="size-4" />
              </div>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">{BRAND.name}</span>
                <span className="truncate text-xs text-muted-foreground">
                  {roleLabel}
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {navConfig ? (
                <>
                  {standalone.map((item) => (
                    <SidebarMenuItem key={item.href}>
                      <SidebarMenuButton
                        tooltip={item.title}
                        isActive={isNavItemActive(pathname, item.href)}
                        render={<Link href={item.href} />}
                      >
                        <item.icon />
                        <span>{item.title}</span>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                  {groups.map((group) => {
                    const isOpen = openGroups[group.title] ?? false;
                    const groupActive = groupHasActiveChild(pathname, group);
                    return (
                      <Collapsible
                        key={group.title}
                        open={isOpen}
                        onOpenChange={(open) =>
                          setOpenGroups((prev) => ({
                            ...prev,
                            [group.title]: open,
                          }))
                        }
                        className="group/collapsible"
                      >
                        <SidebarMenuItem>
                          <CollapsibleTrigger
                            render={
                              <SidebarMenuButton
                                tooltip={group.title}
                                isActive={groupActive}
                                className="data-[state=open]:bg-sidebar-accent/50"
                              />
                            }
                          >
                            <group.icon />
                            <span>{group.title}</span>
                            <IconChevronRight
                              className={cn(
                                "ml-auto size-4 shrink-0 text-muted-foreground transition-transform duration-200",
                                isOpen && "rotate-90",
                              )}
                            />
                          </CollapsibleTrigger>
                          <CollapsibleContent>
                            <SidebarMenuSub>
                              {group.items.map((item) => (
                                <SidebarMenuSubItem key={item.href}>
                                  <SidebarMenuSubButton
                                    isActive={isNavItemActive(
                                      pathname,
                                      item.href,
                                    )}
                                    render={<Link href={item.href} />}
                                  >
                                    <item.icon />
                                    <span>{item.title}</span>
                                  </SidebarMenuSubButton>
                                </SidebarMenuSubItem>
                              ))}
                            </SidebarMenuSub>
                          </CollapsibleContent>
                        </SidebarMenuItem>
                      </Collapsible>
                    );
                  })}
                </>
              ) : (
                flatItems.map((item) => (
                  <SidebarMenuItem key={item.href}>
                    <SidebarMenuButton
                      tooltip={item.title}
                      isActive={isNavItemActive(pathname, item.href)}
                      render={<Link href={item.href} />}
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <PortalUserMenu
          variant="sidebar"
          hideProfile={hideFooterProfile}
        />
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
