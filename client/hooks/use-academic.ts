"use client";

import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import type { PaginatedResponse } from "@/types/api";

export interface Department {
  id: string;
  name: string;
  code: string;
  description: string | null;
}

export interface Course {
  id: string;
  department_id: string;
  name: string;
  code: string;
  credits: number;
  course_type: string;
}

export interface FacultyMember {
  id: string;
  name: string;
  email: string | null;
  department_id: string;
  user_id: string;
}

export interface Program {
  id: string;
  department_id: string;
  name: string;
  code: string;
  duration_semesters: number;
}

export interface AtRiskStudent {
  student_id: string;
  student_name: string;
  roll_number: string;
  risk_score: number;
  risk_level: string;
  risk_factors: string[];
  recommendations: string[];
  department_name?: string | null;
  program_name?: string | null;
  semester?: number | null;
  attendance_percentage?: number | null;
  cgpa?: number | null;
  backlog_count?: number | null;
  performance_trend?: string | null;
}

export interface SemesterResult {
  id: string;
  student_id: string;
  student_name?: string | null;
  roll_number?: string | null;
  semester_id: string;
  sgpa: number | null;
  cgpa: number | null;
  backlog_count: number;
  current_failed_courses: number;
  low_performance_course_count: number;
  performance_trend: string;
}

export function useDepartments(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["departments", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<Department>>(
        `/departments?page=${page}&limit=${limit}`,
      ),
  });
}

export function useCourses(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["courses", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<Course>>(
        `/courses?page=${page}&limit=${limit}`,
      ),
  });
}

export function usePrograms(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["programs", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<Program>>(
        `/programs?page=${page}&limit=${limit}`,
      ),
  });
}

export function useFaculty(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["faculty", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<FacultyMember>>(
        `/faculty?page=${page}&limit=${limit}`,
      ),
  });
}

export interface AtRiskListFilters {
  department_name?: string;
  semester?: number;
  risk_level?: string;
  performance_trend?: string;
  attendance_band?: string;
  cgpa_band?: string;
}

function atRiskFiltersToQuery(filters?: AtRiskListFilters): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  if (filters.department_name) params.set("department_name", filters.department_name);
  if (filters.semester) params.set("semester", String(filters.semester));
  if (filters.risk_level) params.set("risk_level", filters.risk_level);
  if (filters.performance_trend) params.set("performance_trend", filters.performance_trend);
  if (filters.attendance_band) params.set("attendance_band", filters.attendance_band);
  if (filters.cgpa_band) params.set("cgpa_band", filters.cgpa_band);
  const qs = params.toString();
  return qs ? `&${qs}` : "";
}

export function useAtRiskStudents(
  page = 1,
  limit = 50,
  filters?: AtRiskListFilters,
) {
  return useQuery({
    queryKey: ["at-risk", page, limit, filters],
    queryFn: () =>
      apiFetch<PaginatedResponse<AtRiskStudent>>(
        `/at-risk?page=${page}&limit=${limit}${atRiskFiltersToQuery(filters)}`,
      ),
  });
}

export function useSemesterResults(studentId?: string, enabled = true) {
  return useQuery({
    queryKey: ["results", "semester", studentId],
    queryFn: () => {
      const params = studentId ? `?student_id=${studentId}` : "";
      return apiFetch<PaginatedResponse<SemesterResult>>(
        `/results/semester${params}`,
      );
    },
    enabled,
  });
}

export interface ParentMe {
  id: string;
  name: string;
  user_id: string;
  linked_student_ids: string[];
}

export function useMyParentProfile() {
  return useQuery({
    queryKey: ["parents", "me"],
    queryFn: () => apiFetch<ParentMe>("/parents/me"),
  });
}
