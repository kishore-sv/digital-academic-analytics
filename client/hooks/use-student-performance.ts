"use client";

import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";

export interface CoursePerformanceRow {
  course_id: string;
  course_name: string;
  course_code: string;
  credits: number;
  marks: number | null;
  grade: string | null;
  grade_point: number | null;
  status: string | null;
  attendance_percentage: number | null;
}

export interface SemesterPerformanceDetail {
  semester_id: string;
  semester_number: number;
  semester_name: string;
  sgpa: number | null;
  cgpa: number | null;
  average_marks: number | null;
  average_attendance: number | null;
  passed_courses: number;
  failed_courses: number;
  backlogs: number;
  strongest_course: string | null;
  weakest_course: string | null;
  courses: CoursePerformanceRow[];
}

export interface StudentPerformance {
  student_id: string;
  student_name: string;
  roll_number: string;
  current_cgpa: number | null;
  current_sgpa: number | null;
  total_credits: number;
  backlogs: number;
  semesters: SemesterPerformanceDetail[];
}

export interface GoalGuidance {
  current_cgpa: number | null;
  target_cgpa: number | null;
  recent_sgpa: number[];
  predicted_performance: number | null;
  required_sgpa_hint: number | null;
  guidance: string[];
}

export function useStudentPerformance(studentId?: string) {
  const path = studentId
    ? `/students/${studentId}/performance`
    : "/students/me/performance";
  return useQuery({
    queryKey: ["student-performance", studentId ?? "me"],
    queryFn: () => apiFetch<StudentPerformance>(path),
  });
}

export function useGoalGuidance(targetCgpa?: number) {
  const params = targetCgpa != null ? `?target_cgpa=${targetCgpa}` : "";
  return useQuery({
    queryKey: ["goal-guidance", targetCgpa],
    queryFn: () => apiFetch<GoalGuidance>(`/students/me/goal-guidance${params}`),
    enabled: targetCgpa != null && targetCgpa > 0,
  });
}
