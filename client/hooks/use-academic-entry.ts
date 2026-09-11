"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";

export interface Assessment {
  id: string;
  course_id: string;
  name: string;
  assessment_type: string;
  max_marks: number;
}

export interface RosterStudent {
  enrollment_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  attendance_percentage: number | null;
  mark_id: string | null;
  marks_obtained: number | null;
}

export interface MarksRoster {
  assessment_id: string;
  assessment_name: string;
  max_marks: number;
  students: RosterStudent[];
}

export interface AssessmentColumn {
  id: string;
  name: string;
  assessment_type: string;
  max_marks: number;
}

export interface MarkCell {
  assessment_id: string;
  mark_id: string | null;
  marks_obtained: number | null;
}

export interface MarksGridStudent {
  enrollment_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  section: string | null;
  attendance_percentage: number | null;
  marks: MarkCell[];
  total_marks: number | null;
  grade: string | null;
  status: string | null;
}

export interface MarksGrid {
  course_id: string;
  course_name: string;
  course_code: string;
  course_type: string;
  assessments: AssessmentColumn[];
  students: MarksGridStudent[];
}

export interface AttendanceRosterStudent {
  enrollment_id: string;
  student_id: string;
  student_name: string;
  roll_number: string;
  section: string | null;
  attendance_percentage: number | null;
}

export interface AttendanceRoster {
  course_id: string;
  course_name: string;
  course_code: string;
  students: AttendanceRosterStudent[];
}

export interface MarksEntryFilterParams {
  course_id?: string;
  semester_id?: string;
  department_id?: string;
  program_id?: string;
  section?: string;
  search?: string;
}

function buildQueryParams(filters: MarksEntryFilterParams): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  return params.toString();
}

export function useAssessments(courseId?: string) {
  return useQuery({
    queryKey: ["assessments", courseId],
    queryFn: () =>
      apiFetch<{ data: Assessment[] }>(
        `/assessments?course_id=${courseId}&limit=50`,
      ),
    enabled: !!courseId,
  });
}

export function useMarksRoster(
  courseId?: string,
  assessmentId?: string,
  semesterId?: string,
) {
  const params = new URLSearchParams();
  if (courseId) params.set("course_id", courseId);
  if (assessmentId) params.set("assessment_id", assessmentId);
  if (semesterId) params.set("semester_id", semesterId);
  return useQuery({
    queryKey: ["marks-roster", courseId, assessmentId, semesterId],
    queryFn: () =>
      apiFetch<MarksRoster>(`/assessments/roster?${params.toString()}`),
    enabled: !!courseId && !!assessmentId,
  });
}

export function useMarksGrid(filters: MarksEntryFilterParams, enabled = true) {
  const qs = buildQueryParams(filters);
  return useQuery({
    queryKey: ["marks-grid", filters],
    queryFn: () => apiFetch<MarksGrid>(`/assessments/marks-grid?${qs}`),
    enabled: enabled && !!filters.course_id,
  });
}

export function useAttendanceRoster(filters: MarksEntryFilterParams, enabled = true) {
  const qs = buildQueryParams(filters);
  return useQuery({
    queryKey: ["attendance-roster", filters],
    queryFn: () => apiFetch<AttendanceRoster>(`/attendance/roster?${qs}`),
    enabled: enabled && !!filters.course_id,
  });
}

export function useBulkMarksGridMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (vars: {
      entries: { enrollment_id: string; assessment_id: string; marks_obtained: number | null }[];
      trigger_predictions?: boolean;
    }) =>
      apiFetch("/assessments/marks/bulk-grid", {
        method: "POST",
        body: JSON.stringify({
          entries: vars.entries,
          recalculate_results: true,
          trigger_predictions: vars.trigger_predictions ?? false,
        }),
      }),
    ...mergeMutationHandlers(
      {
        showSuccess: false,
        successMessage: "",
        errorMessage: "Failed to save marks.",
      },
      {
        onSuccess: () => {
          qc.invalidateQueries({ queryKey: ["marks-grid"] });
          qc.invalidateQueries({ queryKey: ["marks-roster"] });
        },
      },
    ),
  });
}

export function useBulkMarksMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (entries: { enrollment_id: string; assessment_id: string; marks_obtained: number }[]) =>
      apiFetch("/assessments/marks/bulk", {
        method: "POST",
        body: JSON.stringify({ entries }),
      }),
    ...mergeMutationHandlers(
      {
        showSuccess: false,
        successMessage: "",
        errorMessage: "Failed to save marks.",
      },
      {
        onSuccess: () => {
          qc.invalidateQueries({ queryKey: ["marks-roster"] });
        },
      },
    ),
  });
}

export function useBulkAttendanceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (entries: { enrollment_id: string; attendance_percentage: number }[]) =>
      apiFetch("/attendance/bulk", {
        method: "POST",
        body: JSON.stringify({ entries }),
      }),
    ...mergeMutationHandlers(
      {
        showSuccess: false,
        successMessage: "",
        errorMessage: "Failed to save attendance.",
      },
      {
        onSuccess: () => {
          qc.invalidateQueries({ queryKey: ["marks-roster"] });
          qc.invalidateQueries({ queryKey: ["attendance-roster"] });
        },
      },
    ),
  });
}

export function useRegeneratePredictions() {
  return useMutation({
    mutationFn: () =>
      apiFetch<{ regenerated_count: number }>("/predictions/regenerate?replace_existing=true", {
        method: "POST",
      }),
    ...mergeMutationHandlers<{ regenerated_count: number }>({
      successMessage: (data) =>
        `Regenerated ${data.regenerated_count} predictions.`,
      errorMessage: "Failed to regenerate predictions.",
    }),
  });
}
