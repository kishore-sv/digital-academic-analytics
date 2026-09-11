"use client";

import { useMutation } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { AllPredictions, PerformanceFeatures } from "@/types/prediction";

export function usePredictAll() {
  return useMutation<AllPredictions, Error, PerformanceFeatures>({
    mutationFn: (features) =>
      apiFetch<AllPredictions>("/predictions/all", {
        method: "POST",
        body: JSON.stringify(features),
      }),
    ...mergeMutationHandlers<AllPredictions>({
      successMessage: "Prediction completed successfully.",
      errorMessage: "Prediction failed.",
    }),
  });
}

export function usePredictForStudent(options?: { silent?: boolean }) {
  const silent = options?.silent ?? false;
  return useMutation<AllPredictions, Error, string>({
    mutationFn: (studentId) =>
      apiFetch<AllPredictions>("/predictions/student", {
        method: "POST",
        body: JSON.stringify({ student_id: studentId }),
      }),
    ...mergeMutationHandlers<AllPredictions>({
      showSuccess: !silent,
      showError: !silent,
      successMessage: "Student prediction completed successfully.",
      errorMessage: "Failed to run student prediction.",
    }),
  });
}
