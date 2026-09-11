"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import {
  ReportFiltersBar,
  filtersFromSearchParams,
  filtersToSearchParams,
} from "@/components/analytics/report-filters-bar";
import { ReportPreview } from "@/components/analytics/report-preview";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/layout/page-header";
import { useReportPreview } from "@/hooks/use-report-preview";
import { useReportDownloads } from "@/hooks/use-reports";
import type { AnalyticsFilters } from "@/types/analytics";

export function FacultyReportsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [draftFilters, setDraftFilters] = useState<AnalyticsFilters>({});
  const [appliedFilters, setAppliedFilters] = useState<AnalyticsFilters>({});
  const { downloadInstitutionalPdf } = useReportDownloads();
  const preview = useReportPreview(appliedFilters, true);

  useEffect(() => {
    const fromUrl = filtersFromSearchParams(searchParams);
    setDraftFilters(fromUrl);
    setAppliedFilters(fromUrl);
  }, [searchParams]);

  const applyFilters = useCallback(() => {
    const params = filtersToSearchParams(draftFilters);
    router.replace(`/faculty/reports${params.toString() ? `?${params.toString()}` : ""}`);
    setAppliedFilters(draftFilters);
  }, [draftFilters, router]);

  const resetFilters = useCallback(() => {
    router.replace("/faculty/reports");
    setDraftFilters({});
    setAppliedFilters({});
  }, [router]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Generate scoped reports for your assigned students."
      />

      <ReportFiltersBar
        value={draftFilters}
        onChange={setDraftFilters}
        onApply={applyFilters}
        onReset={resetFilters}
      />

      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-base">Report Preview</CardTitle>
          <Button
            onClick={() =>
              downloadInstitutionalPdf({ filters: appliedFilters, scoped: true })
            }
            disabled={!appliedFilters.academic_year_id || preview.isLoading}
          >
            Download PDF
          </Button>
        </CardHeader>
        <CardContent>
          {!appliedFilters.academic_year_id && (
            <EmptyState
              title="Select filters"
              description="Choose an academic year and click Apply Filters to preview the report."
            />
          )}
          {appliedFilters.academic_year_id && preview.isLoading && <LoadingState />}
          {appliedFilters.academic_year_id && preview.error && (
            <ErrorState description="Unable to load report preview." />
          )}
          {appliedFilters.academic_year_id && preview.data && (
            <ReportPreview data={preview.data} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
