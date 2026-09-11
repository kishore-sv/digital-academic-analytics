"use client";

import { API_BASE_URL, apiFetch } from "@/lib/api";
import {
  getErrorMessage,
  showErrorToast,
  showSuccessToast,
} from "@/lib/toast";
import type { AnalyticsFilters } from "@/types/analytics";
import { filtersToQuery } from "@/types/analytics";
import type { ReportContext } from "@/types/report";

export interface ReportDownloadOptions {
  filters?: AnalyticsFilters;
  includeCharts?: boolean;
  scoped?: boolean;
}

function buildReportQuery({ filters, includeCharts }: ReportDownloadOptions = {}) {
  const params = new URLSearchParams(
    filters ? filtersToQuery(filters).replace(/^\?/, "") : "",
  );
  if (includeCharts) {
    params.set("include_charts", "true");
  }
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

async function fetchReportFilename(
  options?: ReportDownloadOptions,
): Promise<string> {
  const base = options?.scoped
    ? "/reports/scoped/institutional/data"
    : "/reports/institutional/data";
  const data = await apiFetch<ReportContext>(
    `${base}${buildReportQuery({ filters: options?.filters })}`,
  );
  const parts = [
    data.header.institution_name.replace(/\s+/g, "-"),
    data.header.filters.academic_year !== "All Academic Years"
      ? data.header.filters.academic_year
      : null,
    data.header.filters.semester !== "All Semesters"
      ? data.header.filters.semester.replace(/\s+/g, "-")
      : null,
    data.header.filters.department !== "Institution"
      ? data.header.filters.department.replace(/\s+/g, "-")
      : null,
    "Academic-Report",
  ].filter(Boolean);
  return `${parts.join("-")}.pdf`;
}

async function downloadReport(path: string, filename: string) {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      credentials: "include",
    });
    if (!response.ok) {
      let message = "Failed to download report";
      try {
        const body = await response.json();
        if (typeof body?.detail === "string") {
          message = body.detail;
        }
      } catch {
        // ignore non-JSON error bodies
      }
      throw new Error(message);
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
    showSuccessToast({ description: `${filename} downloaded successfully.` });
  } catch (error) {
    showErrorToast({
      description: getErrorMessage(error, "Failed to download report."),
    });
    throw error;
  }
}

export function useReportDownloads() {
  return {
    downloadInstitutional: (options?: ReportDownloadOptions) =>
      downloadReport(
        `/reports/institutional${buildReportQuery(options)}`,
        "institutional-report.html",
      ),
    downloadInstitutionalPdf: async (options?: ReportDownloadOptions) => {
      const pdfPath = options?.scoped
        ? `/reports/scoped/institutional/pdf${buildReportQuery({ ...options, includeCharts: true })}`
        : `/reports/institutional/pdf${buildReportQuery({ ...options, includeCharts: true })}`;
      const filename = await fetchReportFilename(options);
      return downloadReport(pdfPath, filename);
    },
    downloadAtRisk: (options?: ReportDownloadOptions) =>
      downloadReport(
        `/reports/at-risk${buildReportQuery(options)}`,
        "at-risk-report.html",
      ),
    downloadAtRiskPdf: (options?: ReportDownloadOptions) =>
      downloadReport(
        `/reports/at-risk/pdf${buildReportQuery({ ...options, includeCharts: true })}`,
        "at-risk-report.pdf",
      ),
    downloadStudentReport: (studentId: string) =>
      downloadReport(
        `/reports/student/${studentId}`,
        `student-${studentId}-report.html`,
      ),
  };
}
