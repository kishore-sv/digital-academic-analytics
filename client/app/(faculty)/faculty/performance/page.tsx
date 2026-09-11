"use client";

import { useMemo, useState } from "react";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import {
  filterSemesterResults,
  PerformanceTableFiltersBar,
  type PerformanceTableFilters,
} from "@/components/analytics/performance-table-filters";
import {
  SemesterResultsTable,
  semesterResultsSummary,
} from "@/components/analytics/semester-results-table";
import { StatCard } from "@/components/analytics/stat-card";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useSemesterResults } from "@/hooks/use-academic";

export default function FacultyPerformancePage() {
  const [filters, setFilters] = useState<PerformanceTableFilters>({});
  const { data, isLoading, error } = useSemesterResults();
  const results = data?.data ?? [];
  const filteredResults = useMemo(
    () => filterSemesterResults(results, filters),
    [results, filters],
  );
  const summary = useMemo(() => semesterResultsSummary(results), [results]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Student Performance"
        description="Track CGPA, SGPA, backlogs, and performance trends for your assigned students."
      />

      {isLoading && <LoadingState />}
      {error && (
        <ErrorState description="Unable to load student performance data." />
      )}

      {!isLoading && !error && results.length === 0 && (
        <EmptyState
          title="No performance data"
          description="Semester results will appear here once they are recorded for your students."
        />
      )}

      {!isLoading && !error && results.length > 0 && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Assigned Students"
              value={summary.studentCount}
              description="Students with recorded results"
            />
            <StatCard
              title="Average CGPA"
              value={summary.avgCgpa?.toFixed(2) ?? "—"}
              description="Across displayed results"
            />
            <StatCard
              title="With Backlogs"
              value={summary.withBacklogs}
              description="Students carrying backlogs"
            />
            <StatCard
              title="Declining Trend"
              value={summary.declining}
              description="Students showing decline"
            />
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Performance Overview</CardTitle>
              <p className="text-sm text-muted-foreground">
                Rows highlighted in amber indicate backlogs or a declining trend.
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              <PerformanceTableFiltersBar value={filters} onChange={setFilters} />
              {filteredResults.length === 0 ? (
                <EmptyState
                  title="No students match filters"
                  description="Try adjusting or clearing the filters above."
                />
              ) : (
                <>
                  <p className="text-sm text-muted-foreground">
                    Showing {filteredResults.length} of {results.length} results
                  </p>
                  <SemesterResultsTable
                    results={filteredResults}
                    highlightConcerns
                  />
                </>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
