import { formatYearNumber } from "@/lib/academic-display";
import type { MarksEntryFilters } from "@/components/academic/marks-entry-filters";

export const YEAR_OF_STUDY_OPTIONS = [1, 2, 3, 4] as const;

export function semesterNumbersForYear(yearNumber: number): number[] {
  return [yearNumber * 2 - 1, yearNumber * 2];
}

export function yearNumberFromSemesterNumber(semesterNumber: number): number {
  return Math.ceil(semesterNumber / 2);
}

export function applyMarksFilterCascade(
  prev: MarksEntryFilters,
  partial: Partial<MarksEntryFilters>,
): MarksEntryFilters {
  const next: MarksEntryFilters = { ...prev, ...partial };

  if (
    partial.department_id !== undefined &&
    partial.department_id !== prev.department_id
  ) {
    next.program_id = undefined;
    next.batch_id = undefined;
    next.class_group_id = undefined;
    next.section_id = undefined;
    next.course_id = undefined;
    next.assessment_id = undefined;
  }

  if (partial.program_id !== undefined && partial.program_id !== prev.program_id) {
    next.batch_id = undefined;
    next.class_group_id = undefined;
    next.section_id = undefined;
    next.course_id = undefined;
    next.assessment_id = undefined;
  }

  if (partial.batch_id !== undefined && partial.batch_id !== prev.batch_id) {
    next.class_group_id = undefined;
    next.section_id = undefined;
  }

  if (
    partial.class_group_id !== undefined &&
    partial.class_group_id !== prev.class_group_id
  ) {
    next.section_id = undefined;
  }

  if (
    partial.academic_year_id !== undefined &&
    partial.academic_year_id !== prev.academic_year_id
  ) {
    next.semester_id = undefined;
    next.year_number = undefined;
    next.course_id = undefined;
    next.assessment_id = undefined;
  }

  if (partial.semester_id !== undefined && partial.semester_id !== prev.semester_id) {
    next.course_id = undefined;
    next.assessment_id = undefined;
  }

  if (partial.year_number !== undefined && partial.year_number !== prev.year_number) {
    next.course_id = undefined;
    next.assessment_id = undefined;
  }

  if (partial.course_id !== undefined && partial.course_id !== prev.course_id) {
    next.assessment_id = undefined;
  }

  return next;
}

export interface MarksFilterSummaryLabels {
  academicYear?: string;
  semester?: string;
  department?: string;
  yearOfStudy?: string;
  program?: string;
  batch?: string;
  classGroup?: string;
  section?: string;
  course?: string;
  assessment?: string;
}

export function buildMarksFilterSummary(
  filters: MarksEntryFilters,
  labels: MarksFilterSummaryLabels,
): string[] {
  const parts: string[] = [];
  if (labels.academicYear) parts.push(labels.academicYear);
  if (labels.semester) parts.push(labels.semester);
  if (labels.department) parts.push(labels.department);
  if (labels.yearOfStudy) parts.push(labels.yearOfStudy);
  if (labels.program) parts.push(labels.program);
  if (labels.batch) parts.push(labels.batch);
  if (labels.classGroup) parts.push(labels.classGroup);
  if (labels.section) parts.push(labels.section);
  if (labels.course) parts.push(labels.course);
  if (labels.assessment) parts.push(labels.assessment);
  if (filters.search) parts.push(`Search: ${filters.search}`);
  return parts;
}

export function formatYearOfStudyOption(yearNumber: number): string {
  return formatYearNumber(yearNumber);
}
