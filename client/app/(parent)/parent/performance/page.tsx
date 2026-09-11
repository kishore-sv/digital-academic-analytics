"use client";

import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { SemesterResultsTable } from "@/components/analytics/semester-results-table";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useMyParentProfile, useSemesterResults } from "@/hooks/use-academic";

export default function ParentPerformancePage() {
  const { data: parent } = useMyParentProfile();
  const childId = parent?.linked_student_ids[0];
  const { data, isLoading, error } = useSemesterResults(childId, !!childId);
  const results = data?.data ?? [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Child Performance"
        description="Semester academic results for your linked child."
      />
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Performance History</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && <LoadingState />}
          {error && (
            <ErrorState description="Unable to load performance data." />
          )}
          {!isLoading && !error && results.length === 0 && (
            <EmptyState title="No performance data" />
          )}
          {!isLoading && !error && results.length > 0 && (
            <SemesterResultsTable results={results} highlightConcerns />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
