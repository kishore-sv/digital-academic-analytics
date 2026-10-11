"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { PaginatedResponse } from "@/types/api";

export interface AcademicYear {
  id: string;
  name: string;
  is_current: boolean;
}

export interface Semester {
  id: string;
  academic_year_id: string;
  number: number;
  name: string;
  year_number: number;
  year_label?: string | null;
}

export interface Batch {
  id: string;
  program_id: string;
  admission_year: number;
  code: string;
  name: string;
  is_active: boolean;
}

export interface ClassGroup {
  id: string;
  batch_id: string;
  year_number: number;
  code: string;
  name: string;
}

export interface Section {
  id: string;
  class_group_id: string;
  code: string;
  name: string;
  is_active: boolean;
}

export interface ProgramCourse {
  id: string;
  program_id: string;
  course_id: string;
  semester_number: number;
}

export interface FacultyCourse {
  id: string;
  faculty_id: string;
  course_id: string;
  semester_id: string;
  section_id: string | null;
}

export interface Enrollment {
  id: string;
  student_id: string;
  course_id: string;
  semester_id: string;
  section_id: string | null;
  attendance_percentage: number | null;
  study_hours_per_week: number | null;
  assignment_completion_pct: number | null;
}

export function useAcademicYears() {
  return useQuery({
    queryKey: ["academic", "years"],
    queryFn: () => apiFetch<AcademicYear[]>("/academic/years"),
  });
}

export function useSemesters(academicYearId?: string) {
  return useQuery({
    queryKey: ["academic", "semesters", academicYearId],
    queryFn: () =>
      apiFetch<Semester[]>(
        academicYearId
          ? `/academic/semesters?academic_year_id=${academicYearId}`
          : "/academic/semesters",
      ),
    enabled: academicYearId !== "",
  });
}

export function useBatches(programId?: string) {
  return useQuery({
    queryKey: ["batches", programId],
    queryFn: () =>
      apiFetch<PaginatedResponse<Batch>>(
        `/batches?limit=100${programId ? `&program_id=${programId}` : ""}`,
      ),
    enabled: Boolean(programId),
  });
}

export function useClassGroups(batchId?: string, yearNumber?: number) {
  return useQuery({
    queryKey: ["class-groups", batchId, yearNumber],
    queryFn: () => {
      const params = new URLSearchParams({ limit: "100" });
      if (batchId) params.set("batch_id", batchId);
      if (yearNumber) params.set("year_number", String(yearNumber));
      return apiFetch<PaginatedResponse<ClassGroup>>(
        `/class-groups?${params.toString()}`,
      );
    },
    enabled: Boolean(batchId),
  });
}

export function useSections(classGroupId?: string) {
  return useQuery({
    queryKey: ["sections", classGroupId],
    queryFn: () =>
      apiFetch<PaginatedResponse<Section>>(
        classGroupId
          ? `/sections?limit=100&class_group_id=${classGroupId}`
          : "/sections?limit=100",
      ),
    enabled: classGroupId !== "",
  });
}

export function useProgramCourses(programId?: string, semesterNumber?: number) {
  return useQuery({
    queryKey: ["program-courses", programId, semesterNumber],
    queryFn: () => {
      const params = new URLSearchParams({ limit: "100" });
      if (programId) params.set("program_id", programId);
      if (semesterNumber) params.set("semester_number", String(semesterNumber));
      return apiFetch<PaginatedResponse<ProgramCourse>>(
        `/program-courses?${params.toString()}`,
      );
    },
    enabled: Boolean(programId),
  });
}

export function useFacultyCourses(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["faculty-courses", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<FacultyCourse>>(
        `/faculty-courses?page=${page}&limit=${limit}`,
      ),
  });
}

export function useEnrollments(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["enrollments", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<Enrollment>>(
        `/results/enrollments?page=${page}&limit=${limit}`,
      ),
  });
}

function useStructureMutation<T>(
  key: string[],
  path: string,
  messages: { success: string; error: string },
) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: Record<string, unknown>) =>
      apiFetch<T>(path, { method: "POST", body: JSON.stringify(body) }),
    ...mergeMutationHandlers(
      { successMessage: messages.success, errorMessage: messages.error },
      { onSuccess: () => qc.invalidateQueries({ queryKey: key }) },
    ),
  });
}

export function useCreateAcademicYear() {
  return useStructureMutation<AcademicYear>(
    ["academic", "years"],
    "/academic/years",
    { success: "Academic year created.", error: "Failed to create academic year." },
  );
}

export function useCreateSemester() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: {
      academic_year_id: string;
      number: number;
      name: string;
      year_number: number;
    }) =>
      apiFetch<Semester>("/academic/semesters", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      { successMessage: "Semester created.", errorMessage: "Failed to create semester." },
      {
        onSuccess: () => {
          qc.invalidateQueries({ queryKey: ["academic", "semesters"] });
        },
      },
    ),
  });
}

export function useCreateBatch() {
  return useStructureMutation<Batch>(
    ["batches"],
    "/batches",
    { success: "Batch created.", error: "Failed to create batch." },
  );
}

export function useCreateClassGroup() {
  return useStructureMutation<ClassGroup>(
    ["class-groups"],
    "/class-groups",
    { success: "Class group created.", error: "Failed to create class group." },
  );
}

export function useCreateSection() {
  return useStructureMutation<Section>(
    ["sections"],
    "/sections",
    { success: "Section created.", error: "Failed to create section." },
  );
}

export function useCreateProgramCourse() {
  return useStructureMutation<ProgramCourse>(
    ["program-courses"],
    "/program-courses",
    { success: "Curriculum mapping created.", error: "Failed to create mapping." },
  );
}

export function useCreateFacultyCourse() {
  return useStructureMutation<FacultyCourse>(
    ["faculty-courses"],
    "/faculty-courses",
    { success: "Faculty assignment created.", error: "Failed to create assignment." },
  );
}

export function useCreateEnrollment() {
  return useStructureMutation<Enrollment>(
    ["enrollments"],
    "/results/enrollments",
    { success: "Enrollment created.", error: "Failed to create enrollment." },
  );
}
