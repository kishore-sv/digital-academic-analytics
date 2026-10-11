"use client";

import {
  IconAlertTriangle,
  IconBook,
  IconBuilding,
  IconCalendar,
  IconCalendarEvent,
  IconChartBar,
  IconClipboardList,
  IconDashboard,
  IconFileImport,
  IconFileText,
  IconSchool,
  IconSettings,
  IconStack2,
  IconTrendingUp,
  IconUpload,
  IconUser,
  IconUserCog,
  IconUsers,
  IconUsersGroup,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";
import type { NavItem, SidebarNavConfig } from "@/components/app-sidebar";

export const adminSidebarNav: SidebarNavConfig = {
  standalone: [
    { title: "Dashboard", href: ROUTES.admin.dashboard, icon: IconDashboard },
  ],
  groups: [
    {
      title: "Academic Setup",
      icon: IconSettings,
      defaultOpen: true,
      items: [
        { title: "Departments", href: ROUTES.admin.departments, icon: IconBuilding },
        { title: "Programs", href: ROUTES.admin.programs, icon: IconSchool },
        {
          title: "Academic Years",
          href: ROUTES.admin.academicYears,
          icon: IconCalendar,
        },
        { title: "Semesters", href: ROUTES.admin.semesters, icon: IconCalendarEvent },
        { title: "Batches", href: ROUTES.admin.batches, icon: IconStack2 },
        { title: "Classes", href: ROUTES.admin.classes, icon: IconSchool },
        { title: "Sections", href: ROUTES.admin.sections, icon: IconUsersGroup },
        { title: "Curriculum", href: ROUTES.admin.curriculum, icon: IconBook },
        { title: "Courses", href: ROUTES.admin.courses, icon: IconBook },
      ],
    },
    {
      title: "People",
      icon: IconUsers,
      items: [
        { title: "Students", href: ROUTES.admin.students, icon: IconUsers },
        { title: "Faculty", href: ROUTES.admin.faculty, icon: IconSchool },
        { title: "Parents", href: ROUTES.admin.parents, icon: IconUsersGroup },
      ],
    },
    {
      title: "Academic Management",
      icon: IconSchool,
      items: [
        {
          title: "Enrollments",
          href: ROUTES.admin.enrollments,
          icon: IconClipboardList,
        },
        {
          title: "Faculty Courses",
          href: ROUTES.admin.facultyCourses,
          icon: IconSchool,
        },
        {
          title: "Marks Entry",
          href: ROUTES.admin.marks,
          icon: IconClipboardList,
        },
        {
          title: "Attendance",
          href: ROUTES.admin.attendance,
          icon: IconCalendarEvent,
        },
      ],
    },
    {
      title: "Data Import",
      icon: IconUpload,
      items: [
        { title: "Import Center", href: ROUTES.admin.imports, icon: IconFileImport },
        {
          title: "Import History",
          href: ROUTES.admin.importHistory,
          icon: IconFileText,
        },
      ],
    },
    {
      title: "Performance & Analytics",
      icon: IconChartBar,
      items: [
        { title: "Analytics", href: ROUTES.admin.analytics, icon: IconChartBar },
      ],
    },
    {
      title: "Predictions",
      icon: IconTrendingUp,
      items: [
        {
          title: "Predictions",
          href: ROUTES.admin.predictions,
          icon: IconTrendingUp,
        },
      ],
    },
    {
      title: "Risk & Early Warning",
      icon: IconAlertTriangle,
      items: [
        {
          title: "At-Risk Students",
          href: ROUTES.admin.atRisk,
          icon: IconAlertTriangle,
        },
      ],
    },
    {
      title: "Reports",
      icon: IconFileText,
      items: [
        { title: "Reports", href: ROUTES.admin.reports, icon: IconFileText },
      ],
    },
    {
      title: "Administration",
      icon: IconUserCog,
      items: [
        { title: "Users", href: ROUTES.admin.users, icon: IconUserCog },
        { title: "Profile", href: ROUTES.admin.profile, icon: IconUser },
      ],
    },
  ],
};

function flattenNavConfig(config: SidebarNavConfig): NavItem[] {
  return [
    ...config.standalone,
    ...config.groups.flatMap((g) => g.items),
  ];
}

/** Flat list of all admin routes (e.g. for tests). */
export const adminNavItems: NavItem[] = flattenNavConfig(adminSidebarNav);
