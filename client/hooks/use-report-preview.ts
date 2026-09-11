"use client";

import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import type { AnalyticsFilters } from "@/types/analytics";
import { filtersToQuery } from "@/types/analytics";
import type { ReportContext } from "@/types/report";

export function useReportPreview(filters?: AnalyticsFilters, scoped = false) {
  const base = scoped
    ? "/reports/scoped/institutional/data"
    : "/reports/institutional/data";
  return useQuery({
    queryKey: ["report-preview", scoped, filters],
    queryFn: () =>
      apiFetch<ReportContext>(`${base}${filters ? filtersToQuery(filters) : ""}`),
    enabled: Boolean(filters?.academic_year_id),
  });
}
