"use client";

import {
  IconDashboard,
  IconFileText,
  IconSchool,
  IconTarget,
  IconTrendingUp,
  IconUser,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem } from "@/components/app-sidebar";

export const studentNavItems: NavItem[] = [
  { title: "Dashboard", href: ROUTES.student.dashboard, icon: IconDashboard },
  { title: "Profile", href: ROUTES.student.profile, icon: IconUser },
  { title: "Performance", href: ROUTES.student.performance, icon: IconSchool },
  { title: "Predictions", href: ROUTES.student.predictions, icon: IconTrendingUp },
  { title: "Improvement", href: ROUTES.student.improvement, icon: IconTarget },
  { title: "Goals", href: ROUTES.student.goals, icon: IconTarget },
  { title: "Reports", href: ROUTES.student.reports, icon: IconFileText },
];
