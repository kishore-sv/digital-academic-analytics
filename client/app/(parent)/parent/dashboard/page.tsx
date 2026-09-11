"use client";

import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { PerformanceTrendChart } from "@/components/analytics/charts/performance-trend-chart";
import { ChartShell } from "@/components/analytics/charts/chart-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  useScopedAnalyticsOverview,
  useScopedRiskDistribution,
  usePerformanceTrends,
} from "@/hooks/use-analytics";

export default function ParentDashboardPage() {
  const { data } = useScopedAnalyticsOverview();
  const { data: risk } = useScopedRiskDistribution();
  const { data: trends } = usePerformanceTrends(undefined, true);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Parent Dashboard"
        description="Your child's academic performance at a glance."
      />
      {data && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard title="Predicted Performance" value={data.average_cgpa.toFixed(2)} />
          <StatCard title="Pass Likelihood" value={`${data.pass_percentage}%`} />
          <StatCard title="Academic Risk" value={`${data.at_risk_percentage}%`} />
        </div>
      )}
      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-base">Performance Trend</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isEmpty={!trends?.length}>
              {trends && <PerformanceTrendChart data={trends} />}
            </ChartShell>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Risk Overview</CardTitle></CardHeader>
          <CardContent>
            {risk && <RiskDistributionChart data={risk} />}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
