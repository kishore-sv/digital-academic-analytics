"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { API_BASE_URL, ApiError, apiFetch } from "@/lib/api";
import { mergeMutationHandlers } from "@/lib/toast";
import type { PaginatedResponse } from "@/types/api";

export interface ImportJobSummary {
  available_import_count: number;
  coming_soon_import_count: number;
  total_imports: number;
  last_import_at: string | null;
}

export interface ImportJob {
  id: string;
  import_type: string;
  filename: string;
  status: string;
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_rows: number;
  created_rows: number;
  failed_rows: number;
  error_summary: string | null;
  uploaded_by_email: string | null;
  created_at: string;
}

export interface ImportUploadResponse {
  job_id: string;
  filename: string;
  detected_headers: string[];
  suggested_mapping: Record<string, string>;
  canonical_fields: string[];
  row_count: number;
}

export interface ImportValidationResult {
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_rows: number;
  errors: { row: number; message: string }[];
}

export interface ImportPreview {
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  duplicate_rows: number;
  will_create: number;
  sample_rows: Record<string, string>[];
}

export function useImportSummary() {
  return useQuery({
    queryKey: ["imports", "summary"],
    queryFn: () => apiFetch<ImportJobSummary>("/imports/summary"),
    retry: false,
  });
}

export function useImportJobs(page = 1, limit = 20) {
  return useQuery({
    queryKey: ["imports", "jobs", page, limit],
    queryFn: () =>
      apiFetch<PaginatedResponse<ImportJob>>(
        `/imports/jobs?page=${page}&limit=${limit}`,
      ),
    retry: false,
  });
}

export function useImportJob(jobId: string | undefined) {
  return useQuery({
    queryKey: ["imports", "jobs", jobId],
    queryFn: () => apiFetch<ImportJob>(`/imports/jobs/${jobId}`),
    enabled: Boolean(jobId),
  });
}

export async function downloadImportTemplate(
  apiType: string,
  format: "csv" | "xlsx",
): Promise<Blob> {
  const res = await fetch(
    `${API_BASE_URL}/imports/types/${apiType}/template.${format}`,
    { credentials: "include" },
  );
  if (!res.ok) {
    const text = await res.text();
    throw new ApiError(res.status, text || "Failed to download template");
  }
  return res.blob();
}

export function useUploadImport() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({
      file,
      importType,
    }: {
      file: File;
      importType: string;
    }) => {
      const form = new FormData();
      form.append("file", file);
      form.append("import_type", importType);
      const res = await fetch(`${API_BASE_URL}/imports/jobs`, {
        method: "POST",
        credentials: "include",
        body: form,
      });
      if (!res.ok) {
        let detail = "Upload failed";
        try {
          const body = await res.json();
          detail = body.detail ?? detail;
        } catch {
          /* ignore */
        }
        throw new ApiError(res.status, detail);
      }
      return (await res.json()) as ImportUploadResponse;
    },
    ...mergeMutationHandlers(
      { successMessage: "File uploaded.", errorMessage: "Upload failed." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["imports"] }) },
    ),
  });
}

export function useSaveImportMapping() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      jobId,
      mapping,
    }: {
      jobId: string;
      mapping: Record<string, string>;
    }) =>
      apiFetch(`/imports/jobs/${jobId}/mapping`, {
        method: "PATCH",
        body: JSON.stringify({ column_mapping: mapping }),
      }),
    ...mergeMutationHandlers(
      { successMessage: "Column mapping saved.", errorMessage: "Failed to save mapping." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["imports"] }) },
    ),
  });
}

export function useValidateImport() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (jobId: string) =>
      apiFetch<ImportValidationResult>(`/imports/jobs/${jobId}/validate`, {
        method: "POST",
      }),
    ...mergeMutationHandlers(
      { successMessage: "Validation complete.", errorMessage: "Validation failed." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["imports"] }) },
    ),
  });
}

export function useImportPreview(jobId: string | undefined) {
  return useQuery({
    queryKey: ["imports", "preview", jobId],
    queryFn: () => apiFetch<ImportPreview>(`/imports/jobs/${jobId}/preview`),
    enabled: Boolean(jobId),
  });
}

export function useCommitImport() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (jobId: string) =>
      apiFetch<ImportJob>(`/imports/jobs/${jobId}/commit`, {
        method: "POST",
        body: JSON.stringify({ duplicate_mode: "reject" }),
      }),
    ...mergeMutationHandlers(
      { successMessage: "Import completed.", errorMessage: "Import failed." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["imports"] }) },
    ),
  });
}

export function getImportErrorsUrl(jobId: string): string {
  return `${API_BASE_URL}/imports/jobs/${jobId}/errors.csv`;
}
