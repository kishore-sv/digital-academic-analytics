"use client";

import {
  IconDashboard,
  IconFileText,
  IconSchool,
  IconTarget,
  IconTrendingUp,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem } from "@/components/app-sidebar";

export const parentNavItems: NavItem[] = [
  { title: "Dashboard", href: ROUTES.parent.dashboard, icon: IconDashboard },
  { title: "Performance", href: ROUTES.parent.performance, icon: IconSchool },
  { title: "Predictions", href: ROUTES.parent.predictions, icon: IconTrendingUp },
  { title: "Improvement", href: ROUTES.parent.improvement, icon: IconTarget },
  { title: "Reports", href: ROUTES.parent.reports, icon: IconFileText },
];
