"use client";

import { useState } from "react";
import { AnalyticsFiltersBar } from "@/components/analytics/analytics-filters";
import { AttendanceTrendChart } from "@/components/analytics/charts/attendance-trend-chart";
import { ChartShell } from "@/components/analytics/charts/chart-shell";
import { DepartmentPerformanceChart } from "@/components/analytics/department-performance-chart";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  useAnalyticsOverview,
  useAttendanceTrend,
  useDepartmentAnalytics,
  useRiskDistribution,
} from "@/hooks/use-analytics";
import type { AnalyticsFilters } from "@/types/analytics";

export default function AdminDashboardPage() {
  const { data, isLoading, error } = useAnalyticsOverview();
  const departmentQuery = useDepartmentAnalytics();
  const riskQuery = useRiskDistribution();
  const [trendFilters, setTrendFilters] = useState<AnalyticsFilters>({});
  const trendQuery = useAttendanceTrend(
    trendFilters,
    Boolean(trendFilters.academic_year_id),
  );
  const trendPoints = trendQuery.data?.points ?? [];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Institutional Dashboard"
        description="Overview of academic performance and risk across Demo University."
      />

      {isLoading && <LoadingState />}
      {error && (
        <EmptyState
          title="Unable to load analytics"
          description="Please ensure you are logged in as an institution admin."
        />
      )}
      {data && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Total Students" value={data.total_students} />
          <StatCard title="Total Faculty" value={data.total_faculty} />
          <StatCard title="Departments" value={data.total_departments} />
          <StatCard title="Average CGPA" value={data.average_cgpa.toFixed(2)} />
          <StatCard title="Average SGPA" value={data.average_sgpa.toFixed(2)} />
          <StatCard title="Pass Percentage" value={`${data.pass_percentage}%`} />
          <StatCard title="At-Risk %" value={`${data.at_risk_percentage}%`} />
          <StatCard title="High-Risk Students" value={data.high_risk_count} />
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Risk Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ChartShell
              isLoading={riskQuery.isLoading}
              error={riskQuery.error}
              isEmpty={!riskQuery.data}
            >
              {riskQuery.data && (
                <RiskDistributionChart data={riskQuery.data} />
              )}
            </ChartShell>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Department CGPA</CardTitle>
          </CardHeader>
          <CardContent>
            <ChartShell
              isLoading={departmentQuery.isLoading}
              error={departmentQuery.error}
              isEmpty={!departmentQuery.data?.length}
              emptyTitle="No department CGPA data yet"
            >
              {departmentQuery.data && (
                <DepartmentPerformanceChart departments={departmentQuery.data} />
              )}
            </ChartShell>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader className="gap-3">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
            <div>
              <CardTitle className="text-base">Attendance Trend</CardTitle>
              <p className="text-sm text-muted-foreground">
                Average student attendance over time.
              </p>
            </div>
            <AnalyticsFiltersBar value={trendFilters} onChange={setTrendFilters} />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {!trendFilters.academic_year_id || trendQuery.isLoading ? (
            <LoadingState message="Loading attendance trend..." />
          ) : trendQuery.error ? (
            <div className="space-y-3">
              <ErrorState
                title="Unable to load attendance trend."
                description="The attendance summary could not be loaded."
              />
              <div className="flex justify-center">
                <Button variant="outline" size="sm" onClick={() => trendQuery.refetch()}>
                  Retry
                </Button>
              </div>
            </div>
          ) : trendPoints.length === 0 ? (
            <EmptyState title="No attendance data available for this selection." />
          ) : (
            <>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                <TrendStat label="Current" value={trendQuery.data?.current_percentage} />
                <TrendStat label="Average" value={trendQuery.data?.average_percentage} />
                <TrendStat label="Highest" value={trendQuery.data?.highest_percentage} />
                <TrendStat label="Lowest" value={trendQuery.data?.lowest_percentage} />
              </div>
              <p className="text-xs text-muted-foreground">
                {trendFilters.department_id
                  ? "Average attendance for the selected department and period."
                  : "University average attendance over the selected period."}
              </p>
              <AttendanceTrendChart data={trendPoints} />
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function TrendStat({ label, value }: { label: string; value: number | null | undefined }) {
  return (
    <div>
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="text-lg font-semibold tabular-nums">
        {value == null ? "—" : `${value.toFixed(1)}%`}
      </p>
    </div>
  );
}
