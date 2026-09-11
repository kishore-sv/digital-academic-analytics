"use client";

import { DepartmentPerformanceChart } from "@/components/analytics/department-performance-chart";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { PerformanceTrendChart } from "@/components/analytics/charts/performance-trend-chart";
import { ChartShell } from "@/components/analytics/charts/chart-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  useScopedAnalyticsOverview,
  useScopedDepartmentAnalytics,
  useScopedRiskDistribution,
  usePerformanceTrends,
} from "@/hooks/use-analytics";

export default function FacultyDashboardPage() {
  const { data, isLoading } = useScopedAnalyticsOverview();
  const { data: departments } = useScopedDepartmentAnalytics();
  const { data: risk } = useScopedRiskDistribution();
  const { data: trends } = usePerformanceTrends(undefined, true);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Faculty Dashboard"
        description="Performance overview for your assigned students."
      />
      {data && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Students" value={data.total_students} />
          <StatCard title="Avg CGPA" value={data.average_cgpa.toFixed(2)} />
          <StatCard title="Pass %" value={`${data.pass_percentage}%`} />
          <StatCard title="At-Risk %" value={`${data.at_risk_percentage}%`} />
        </div>
      )}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-base">Risk Distribution</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isLoading={isLoading}>
              {risk && <RiskDistributionChart data={risk} />}
            </ChartShell>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Department Performance</CardTitle></CardHeader>
          <CardContent>
            {departments && departments.length > 0 && (
              <DepartmentPerformanceChart departments={departments} />
            )}
          </CardContent>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle className="text-base">Semester Trends</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isLoading={!trends}>
              {trends && <PerformanceTrendChart data={trends} />}
            </ChartShell>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
