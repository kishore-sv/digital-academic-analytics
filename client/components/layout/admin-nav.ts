"use client";

import {
  IconAlertTriangle,
  IconBook,
  IconBuilding,
  IconChartBar,
  IconDashboard,
  IconFileText,
  IconTrendingUp,
  IconUsers,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem } from "@/components/app-sidebar";

export const adminNavItems: NavItem[] = [
  { title: "Dashboard", href: ROUTES.admin.dashboard, icon: IconDashboard },
  { title: "Students", href: ROUTES.admin.students, icon: IconUsers },
  { title: "Departments", href: ROUTES.admin.departments, icon: IconBuilding },
  { title: "Subjects", href: ROUTES.admin.subjects, icon: IconBook },
  { title: "Analytics", href: ROUTES.admin.analytics, icon: IconChartBar },
  { title: "Predictions", href: ROUTES.admin.predictions, icon: IconTrendingUp },
  { title: "At-Risk", href: ROUTES.admin.atRisk, icon: IconAlertTriangle },
  { title: "Reports", href: ROUTES.admin.reports, icon: IconFileText },
];
