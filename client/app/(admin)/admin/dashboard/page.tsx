"use client";

import { DepartmentPerformanceChart } from "@/components/analytics/department-performance-chart";
import { EmptyState } from "@/components/analytics/empty-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  useAnalyticsOverview,
  useDepartmentAnalytics,
  useRiskDistribution,
} from "@/hooks/use-analytics";

export default function AdminDashboardPage() {
  const { data, isLoading, error } = useAnalyticsOverview();
  const { data: departments } = useDepartmentAnalytics();
  const { data: risk } = useRiskDistribution();

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
            {risk ? <RiskDistributionChart data={risk} /> : <LoadingState />}
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Department CGPA</CardTitle>
          </CardHeader>
          <CardContent>
            {departments && departments.length > 0 ? (
              <DepartmentPerformanceChart departments={departments} />
            ) : (
              <LoadingState />
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
