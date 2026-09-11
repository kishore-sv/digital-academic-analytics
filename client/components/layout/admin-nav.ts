"use client";

import {
  IconAlertTriangle,
  IconBook,
  IconBuilding,
  IconClipboardList,
  IconCalendarEvent,
  IconChartBar,
  IconDashboard,
  IconFileText,
  IconSchool,
  IconTrendingUp,
  IconUserCog,
  IconUsers,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem } from "@/components/app-sidebar";

export const adminNavItems: NavItem[] = [
  { title: "Dashboard", href: ROUTES.admin.dashboard, icon: IconDashboard },
  { title: "Students", href: ROUTES.admin.students, icon: IconUsers },
  { title: "Faculty", href: ROUTES.admin.faculty, icon: IconSchool },
  { title: "Departments", href: ROUTES.admin.departments, icon: IconBuilding },
  { title: "Programs", href: ROUTES.admin.programs, icon: IconSchool },
  { title: "Courses", href: ROUTES.admin.courses, icon: IconBook },
  { title: "Marks Entry", href: ROUTES.admin.marks, icon: IconClipboardList },
  { title: "Attendance", href: ROUTES.admin.attendance, icon: IconCalendarEvent },
  { title: "Analytics", href: ROUTES.admin.analytics, icon: IconChartBar },
  { title: "Predictions", href: ROUTES.admin.predictions, icon: IconTrendingUp },
  { title: "At-Risk", href: ROUTES.admin.atRisk, icon: IconAlertTriangle },
  { title: "Reports", href: ROUTES.admin.reports, icon: IconFileText },
  { title: "Users", href: ROUTES.admin.users, icon: IconUserCog },
];
