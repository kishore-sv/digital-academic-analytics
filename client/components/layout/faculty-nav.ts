"use client";

import {
  IconAlertTriangle,
  IconCalendar,
  IconClipboardList,
  IconDashboard,
  IconFileText,
  IconPencil,
  IconSchool,
  IconTrendingUp,
  IconUsers,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem } from "@/components/app-sidebar";

export const facultyNavItems: NavItem[] = [
  { title: "Dashboard", href: ROUTES.faculty.dashboard, icon: IconDashboard },
  { title: "Students", href: ROUTES.faculty.students, icon: IconUsers },
  { title: "Marks Entry", href: ROUTES.faculty.marks, icon: IconPencil },
  { title: "Attendance", href: ROUTES.faculty.attendance, icon: IconCalendar },
  { title: "Results", href: ROUTES.faculty.results, icon: IconClipboardList },
  { title: "Performance", href: ROUTES.faculty.performance, icon: IconSchool },
  { title: "Predictions", href: ROUTES.faculty.predictions, icon: IconTrendingUp },
  { title: "At-Risk", href: ROUTES.faculty.atRisk, icon: IconAlertTriangle },
  { title: "Reports", href: ROUTES.faculty.reports, icon: IconFileText },
];
