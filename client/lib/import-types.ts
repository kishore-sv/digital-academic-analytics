import type { TablerIcon } from "@tabler/icons-react";
import {
  IconBook,
  IconBuilding,
  IconCalendar,
  IconCalendarEvent,
  IconChartBar,
  IconClipboardList,
  IconFileCertificate,
  IconSchool,
  IconStack2,
  IconUsers,
  IconUsersGroup,
} from "@tabler/icons-react";
import { ROUTES } from "@/lib/constants";

export type ImportCategory = "master" | "academic";
export type ImportAvailability = "available" | "coming_soon";

export interface ImportTypeDefinition {
  key: string;
  title: string;
  description: string;
  category: ImportCategory;
  status: ImportAvailability;
  formats: ("CSV" | "XLSX")[];
  dependsOn?: string[];
  workflowNote?: string;
  icon: TablerIcon;
  apiType: string;
}

const base = ROUTES.admin.imports;

export const IMPORT_TYPE_DEFINITIONS: ImportTypeDefinition[] = [
  {
    key: "departments",
    title: "Department Data",
    description: "Import department information.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    icon: IconBuilding,
    apiType: "departments",
  },
  {
    key: "programs",
    title: "Program Data",
    description: "Import academic programs and their department relationships.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Departments"],
    icon: IconSchool,
    apiType: "programs",
  },
  {
    key: "academic-years",
    title: "Academic Year Data",
    description: "Import academic years such as 2026-27.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    icon: IconCalendar,
    apiType: "academic_years",
  },
  {
    key: "semesters",
    title: "Semester Data",
    description: "Import semester definitions and year-of-study mapping.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Academic Years"],
    icon: IconCalendarEvent,
    apiType: "semesters",
  },
  {
    key: "courses",
    title: "Course Data",
    description: "Import course definitions including theory/lab and credits.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Departments"],
    icon: IconBook,
    apiType: "courses",
  },
  {
    key: "curriculum",
    title: "Curriculum Data",
    description: "Map courses to programs and semester numbers.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Programs", "Courses"],
    icon: IconBook,
    apiType: "program_courses",
  },
  {
    key: "batches",
    title: "Batch Data",
    description: "Import student intake and cohort information.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Programs"],
    icon: IconStack2,
    apiType: "batches",
  },
  {
    key: "classes",
    title: "Class Data",
    description: "Import class groups for batches and years of study.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Batches"],
    icon: IconSchool,
    apiType: "class_groups",
  },
  {
    key: "sections",
    title: "Section Data",
    description: "Import sections such as A, B, and C.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Classes"],
    icon: IconUsersGroup,
    apiType: "sections",
  },
  {
    key: "faculty",
    title: "Faculty Data",
    description: "Import faculty master information.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Departments"],
    icon: IconSchool,
    apiType: "faculty",
  },
  {
    key: "students",
    title: "Student Data",
    description:
      "Import student master information including roll number, program, batch, class, and section.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: [
      "Departments",
      "Programs",
      "Batches",
      "Classes",
      "Sections",
      "Semesters",
    ],
    icon: IconUsers,
    apiType: "students",
  },
  {
    key: "parents",
    title: "Parent / Guardian Data",
    description: "Import parent and guardian information.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Students"],
    icon: IconUsersGroup,
    apiType: "parents",
  },
  {
    key: "enrollments",
    title: "Student Enrollment Data",
    description: "Import student-to-course semester enrollment.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Students", "Courses", "Academic Years", "Semesters"],
    icon: IconClipboardList,
    apiType: "enrollments",
  },
  {
    key: "faculty-assignments",
    title: "Faculty Assignment Data",
    description: "Import faculty-to-course and section assignments.",
    category: "master",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Faculty", "Courses", "Semesters"],
    icon: IconSchool,
    apiType: "faculty_courses",
  },
  {
    key: "attendance",
    title: "Attendance Data",
    description:
      "Import daily or periodic attendance records. One row is one attendance event (present or absent).",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Students", "Courses", "Enrollments", "Semesters"],
    icon: IconCalendarEvent,
    apiType: "attendance",
  },
  {
    key: "ca-marks",
    title: "CA / Internal Marks",
    description:
      "Import continuous assessment and internal marks. One row is one student's mark for one assessment.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: [
      "Students",
      "Courses",
      "Enrollments",
      "Semesters",
      "Assessment",
    ],
    icon: IconChartBar,
    apiType: "ca_marks",
  },
  {
    key: "mid-term-marks",
    title: "Mid-Term Marks",
    description: "Import mid-term examination marks.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: [
      "Students",
      "Courses",
      "Enrollments",
      "Semesters",
      "Assessment",
    ],
    icon: IconChartBar,
    apiType: "mid_term_marks",
  },
  {
    key: "end-sem-marks",
    title: "End-Semester Marks",
    description:
      "Import final examination marks into FINAL assessments. Results are calculated by the system.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: [
      "Students",
      "Courses",
      "Enrollments",
      "Semesters",
      "Assessment",
    ],
    icon: IconChartBar,
    apiType: "end_sem_marks",
  },
  {
    key: "semester-results",
    title: "Semester Results",
    description: "Import official course and semester results.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Student", "Course", "Enrollment", "Semester"],
    workflowNote:
      "Imported SGPA/CGPA are stored as official values. A later marks recalculation may overwrite derived result fields according to the system's result calculation rules.",
    icon: IconFileCertificate,
    apiType: "semester_results",
  },
  {
    key: "backlogs",
    title: "Backlog Data",
    description: "Import historical and current backlog records.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Student", "Course", "Original semester"],
    icon: IconClipboardList,
    apiType: "backlogs",
  },
  {
    key: "backlog-clearance",
    title: "Backlog Clearance",
    description: "Update existing backlog records when they are cleared.",
    category: "academic",
    status: "available",
    formats: ["CSV", "XLSX"],
    dependsOn: ["Existing backlog row", "Clearance semester"],
    icon: IconFileCertificate,
    apiType: "backlog_clearance",
  },
];

export const OPERATIONAL_IMPORT_ORDER = [
  "Attendance",
  "CA / Internal Marks",
  "Mid-Term Marks",
  "End-Semester Marks",
  "Semester Results",
  "Backlog Data",
  "Backlog Clearance",
];

export const MASTER_IMPORT_ORDER = [
  "Departments",
  "Programs",
  "Academic Years",
  "Semesters",
  "Courses",
  "Curriculum",
  "Batches",
  "Classes",
  "Sections",
  "Faculty",
  "Students",
  "Parents",
  "Student Enrollment",
  "Faculty Assignments",
];

export function getImportTypeByKey(
  key: string,
): ImportTypeDefinition | undefined {
  return IMPORT_TYPE_DEFINITIONS.find((t) => t.key === key);
}

export function importWorkflowHref(key: string): string {
  return `${base}/${key}`;
}
