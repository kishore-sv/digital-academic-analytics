"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";

export interface StudentGoal {
  id: string;
  goal_type: string;
  target_value: number;
  current_value: number | null;
  status: string;
  notes: string | null;
}

export interface GoalCreateInput {
  goal_type: "cgpa" | "sgpa";
  target_value: number;
  notes?: string;
}

export interface GoalUpdateInput {
  target_value?: number;
  status?: string;
  notes?: string;
}

export function useGoals() {
  return useQuery({
    queryKey: ["goals"],
    queryFn: () => apiFetch<StudentGoal[]>("/goals"),
  });
}

export function useCreateGoal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (body: GoalCreateInput) =>
      apiFetch<StudentGoal>("/goals", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Goal created successfully.",
        errorMessage: "Failed to create goal.",
      },
      {
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["goals"] }),
      },
    ),
  });
}

export function useUpdateGoal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...body }: GoalUpdateInput & { id: string }) =>
      apiFetch<StudentGoal>(`/goals/${id}`, {
        method: "PATCH",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      {
        successMessage: "Goal updated successfully.",
        errorMessage: "Failed to update goal.",
      },
      {
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["goals"] }),
      },
    ),
  });
}

export function useDeleteGoal() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/goals/${id}`, { method: "DELETE" }),
    ...mergeMutationHandlers(
      {
        successMessage: "Goal deleted successfully.",
        errorMessage: "Failed to delete goal.",
      },
      {
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ["goals"] }),
      },
    ),
  });
}
