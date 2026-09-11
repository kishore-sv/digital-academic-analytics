"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { PaginatedResponse } from "@/types/api";

export interface AdminUser {
  id: string;
  email: string | null;
  role: string;
  institution_id: string;
  is_login_enabled: boolean;
}

export function useUsers(page = 1, limit = 50) {
  return useQuery({
    queryKey: ["users", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<AdminUser>>(
        `/users?page=${page}&limit=${limit}`,
      ),
  });
}

export function useCreateAdminUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: { email: string; password: string }) =>
      apiFetch<AdminUser>("/users", {
        method: "POST",
        body: JSON.stringify({ ...body, role: "institution_admin" }),
      }),
    ...mergeMutationHandlers<AdminUser>(
      {
        successMessage: (user) =>
          `${user.email ?? "Admin user"} was created successfully.`,
        errorMessage: "Failed to create user.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }) },
    ),
  });
}

export function useUpdateUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      is_login_enabled,
    }: {
      id: string;
      is_login_enabled: boolean;
    }) =>
      apiFetch<AdminUser>(`/users/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_login_enabled }),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "User updated successfully.",
        errorMessage: "Failed to update user.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }) },
    ),
  });
}

export function useDeleteUser() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/users/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "User deleted successfully.",
        errorMessage: "Failed to delete user.",
      },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }) },
    ),
  });
}
