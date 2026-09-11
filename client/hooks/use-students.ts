"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { PaginatedResponse } from "@/types/api";

export interface Student {
  id: string;
  roll_number: string;
  name: string;
  department_id: string;
  program_id: string | null;
  semester: number;
  branch: string;
}

export function useStudents(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["students", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<Student>>(
        `/students?page=${page}&limit=${limit}`,
      ),
  });
}

export function useStudent(studentId: string | undefined) {
  return useQuery({
    queryKey: ["students", studentId],
    queryFn: () => apiFetch<Student>(`/students/${studentId}`),
    enabled: !!studentId,
  });
}

export function useMyStudentProfile() {
  return useQuery({
    queryKey: ["students", "me"],
    queryFn: () => apiFetch<Student>("/students/me"),
  });
}

export function useCreateStudent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: {
      name: string;
      roll_number: string;
      password: string;
      department_id: string;
      program_id?: string;
      semester?: number;
      branch?: string;
    }) =>
      apiFetch<Student>("/students", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers<Student>(
      {
        successMessage: (student) =>
          `${student.name} was added successfully.`,
        errorMessage: "Failed to add student.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }) },
    ),
  });
}

export function useUpdateStudent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      ...body
    }: {
      id: string;
      name?: string;
      department_id?: string;
      program_id?: string;
      semester?: number;
      branch?: string;
    }) =>
      apiFetch<Student>(`/students/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Student updated successfully.",
        errorMessage: "Failed to update student.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }) },
    ),
  });
}

export function useDeleteStudent() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/students/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Student deleted successfully.",
        errorMessage: "Failed to delete student.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["students"] }) },
    ),
  });
}
