"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { Course, Department, FacultyMember } from "@/hooks/use-academic";

export interface Program {
  id: string;
  department_id: string;
  name: string;
  code: string;
  duration_semesters: number;
}

export function useCreateDepartment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: { name: string; code: string; description?: string }) =>
      apiFetch<Department>("/departments", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers<Department>(
      {
        successMessage: (dept) => `${dept.name} department created.`,
        errorMessage: "Failed to create department.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }) },
    ),
  });
}

export function useUpdateDepartment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      ...body
    }: {
      id: string;
      name?: string;
      code?: string;
      description?: string;
    }) =>
      apiFetch<Department>(`/departments/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Department updated successfully.",
        errorMessage: "Failed to update department.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }) },
    ),
  });
}

export function useDeleteDepartment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/departments/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Department deleted successfully.",
        errorMessage: "Failed to delete department.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["departments"] }) },
    ),
  });
}

export function useCreateProgram() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: {
      department_id: string;
      name: string;
      code: string;
      duration_semesters?: number;
    }) =>
      apiFetch<Program>("/programs", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers<Program>(
      {
        successMessage: (program) => `${program.name} program created.`,
        errorMessage: "Failed to create program.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["programs"] }) },
    ),
  });
}

export function useUpdateProgram() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      ...body
    }: {
      id: string;
      name?: string;
      code?: string;
      duration_semesters?: number;
    }) =>
      apiFetch<Program>(`/programs/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Program updated successfully.",
        errorMessage: "Failed to update program.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["programs"] }) },
    ),
  });
}

export function useDeleteProgram() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/programs/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Program deleted successfully.",
        errorMessage: "Failed to delete program.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["programs"] }) },
    ),
  });
}

export function useCreateCourse() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: {
      department_id: string;
      name: string;
      code: string;
      credits?: number;
      course_type?: string;
    }) =>
      apiFetch<Course>("/courses", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers<Course>(
      {
        successMessage: (course) => `${course.name} course created.`,
        errorMessage: "Failed to create course.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }) },
    ),
  });
}

export function useUpdateCourse() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      ...body
    }: {
      id: string;
      name?: string;
      code?: string;
      credits?: number;
      course_type?: string;
    }) =>
      apiFetch<Course>(`/courses/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Course updated successfully.",
        errorMessage: "Failed to update course.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }) },
    ),
  });
}

export function useDeleteCourse() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/courses/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Course deleted successfully.",
        errorMessage: "Failed to delete course.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }) },
    ),
  });
}

export function useCreateFaculty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: {
      name: string;
      email: string;
      password: string;
      department_id: string;
    }) =>
      apiFetch<FacultyMember>("/faculty", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers<FacultyMember>(
      {
        successMessage: (faculty) => `${faculty.name} was added successfully.`,
        errorMessage: "Failed to add faculty member.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["faculty"] }) },
    ),
  });
}

export function useUpdateFaculty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      ...body
    }: {
      id: string;
      name?: string;
      department_id?: string;
    }) =>
      apiFetch<FacultyMember>(`/faculty/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Faculty member updated successfully.",
        errorMessage: "Failed to update faculty member.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["faculty"] }) },
    ),
  });
}

export function useDeleteFaculty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/faculty/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Faculty member deleted successfully.",
        errorMessage: "Failed to delete faculty member.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["faculty"] }) },
    ),
  });
}
