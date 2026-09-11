"use client";

import { EmptyState } from "@/components/analytics/empty-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { SemesterResultsTable } from "@/components/analytics/semester-results-table";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useSemesterResults } from "@/hooks/use-academic";

export default function FacultyResultsPage() {
  const { data, isLoading } = useSemesterResults();
  const results = data?.data ?? [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Semester Results"
        description="View semester results for your assigned students."
      />
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Results Overview</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <LoadingState />
          ) : results.length === 0 ? (
            <EmptyState title="No results found" />
          ) : (
            <SemesterResultsTable results={results} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
