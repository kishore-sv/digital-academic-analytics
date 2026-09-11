"use client";

import { useState } from "react";
import { AnalyticsFiltersBar } from "@/components/analytics/analytics-filters";
import { DepartmentPerformanceChart } from "@/components/analytics/department-performance-chart";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { AttendancePerformanceChart } from "@/components/analytics/charts/attendance-performance-chart";
import { CGPADistributionChart } from "@/components/analytics/charts/cgpa-distribution-chart";
import { ChartShell } from "@/components/analytics/charts/chart-shell";
import { DepartmentPassChart } from "@/components/analytics/charts/department-pass-chart";
import { PassFailChart } from "@/components/analytics/charts/pass-fail-chart";
import { PerformanceTrendChart } from "@/components/analytics/charts/performance-trend-chart";
import { PredictionDistributionChart } from "@/components/analytics/charts/prediction-distribution-chart";
import { RiskFactorChart } from "@/components/analytics/charts/risk-factor-chart";
import { StackedRiskChart } from "@/components/analytics/charts/stacked-risk-chart";
import { TrendIndicatorChart } from "@/components/analytics/charts/trend-indicator-chart";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  useAnalyticsOverview,
  useAttendancePerformance,
  useCGPADistribution,
  useDepartmentAnalytics,
  useDepartmentRiskStacks,
  usePassFailTrend,
  usePerformanceIndicators,
  usePerformanceTrends,
  usePredictionPassFail,
  usePredictionPerformance,
  usePredictionRisk,
  useRiskDistribution,
  useRiskFactors,
} from "@/hooks/use-analytics";
import type { AnalyticsFilters } from "@/types/analytics";

function ChartCard({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

export default function AdminAnalyticsPage() {
  const [filters, setFilters] = useState<AnalyticsFilters>({});

  const overview = useAnalyticsOverview(filters);
  const departments = useDepartmentAnalytics(filters);
  const risk = useRiskDistribution(filters);
  const cgpa = useCGPADistribution(filters);
  const trends = usePerformanceTrends(filters);
  const passFail = usePassFailTrend(filters);
  const attendance = useAttendancePerformance(filters);
  const indicators = usePerformanceIndicators(filters);
  const predPerf = usePredictionPerformance(filters);
  const predPF = usePredictionPassFail(filters);
  const predRisk = usePredictionRisk(filters);
  const deptRisk = useDepartmentRiskStacks(filters);
  const riskFactors = useRiskFactors(filters);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Analytics"
        description="Institutional performance, ML predictions, and at-risk insights."
      />
      <AnalyticsFiltersBar value={filters} onChange={setFilters} />

      {overview.data && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard title="Students" value={overview.data.total_students} />
          <StatCard title="Avg CGPA" value={overview.data.average_cgpa.toFixed(2)} />
          <StatCard title="Pass %" value={`${overview.data.pass_percentage}%`} />
          <StatCard title="At-Risk %" value={`${overview.data.at_risk_percentage}%`} />
        </div>
      )}

      <Tabs defaultValue="institutional">
        <TabsList>
          <TabsTrigger value="institutional">Institutional</TabsTrigger>
          <TabsTrigger value="predictions">ML Predictions</TabsTrigger>
          <TabsTrigger value="at-risk">At-Risk</TabsTrigger>
        </TabsList>

        <TabsContent value="institutional" className="mt-4 space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            <ChartCard title="Department CGPA">
              <ChartShell isLoading={departments.isLoading} isEmpty={!departments.data?.length}>
                {departments.data && (
                  <DepartmentPerformanceChart departments={departments.data} />
                )}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Department Pass Rate">
              <ChartShell isLoading={departments.isLoading} isEmpty={!departments.data?.length}>
                {departments.data && <DepartmentPassChart departments={departments.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="CGPA Distribution">
              <ChartShell isLoading={cgpa.isLoading} isEmpty={!cgpa.data?.length}>
                {cgpa.data && <CGPADistributionChart data={cgpa.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Semester Trends">
              <ChartShell isLoading={trends.isLoading} isEmpty={!trends.data?.length}>
                {trends.data && <PerformanceTrendChart data={trends.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Pass / Fail Trend">
              <ChartShell isLoading={passFail.isLoading} isEmpty={!passFail.data?.length}>
                {passFail.data && <PassFailChart data={passFail.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Attendance vs Performance">
              <ChartShell isLoading={attendance.isLoading} isEmpty={!attendance.data?.length}>
                {attendance.data && (
                  <AttendancePerformanceChart data={attendance.data} />
                )}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Performance Trends">
              <ChartShell isLoading={indicators.isLoading}>
                {indicators.data && <TrendIndicatorChart data={indicators.data} />}
              </ChartShell>
            </ChartCard>
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="mt-4 space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            <ChartCard title="Predicted Marks Distribution">
              <ChartShell isLoading={predPerf.isLoading}>
                {predPerf.data && (
                  <PredictionDistributionChart data={predPerf.data.distribution} />
                )}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Pass Probability Distribution">
              <ChartShell isLoading={predPF.isLoading}>
                {predPF.data && (
                  <PredictionDistributionChart
                    data={predPF.data.probability_distribution}
                  />
                )}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Risk Distribution">
              <ChartShell isLoading={predRisk.isLoading}>
                {predRisk.data && (
                  <RiskDistributionChart data={predRisk.data.risk_distribution} />
                )}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Department Risk (Stacked)">
              <ChartShell isLoading={deptRisk.isLoading} isEmpty={!deptRisk.data?.length}>
                {deptRisk.data && <StackedRiskChart data={deptRisk.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Risk Factors">
              <ChartShell isLoading={riskFactors.isLoading} isEmpty={!riskFactors.data?.length}>
                {riskFactors.data && <RiskFactorChart data={riskFactors.data} />}
              </ChartShell>
            </ChartCard>
          </div>
        </TabsContent>

        <TabsContent value="at-risk" className="mt-4 space-y-4">
          {risk.data && (
            <div className="grid gap-4 sm:grid-cols-3">
              <StatCard title="Low Risk" value={risk.data.low} />
              <StatCard title="Medium Risk" value={risk.data.medium} />
              <StatCard title="High Risk" value={risk.data.high} />
            </div>
          )}
          <div className="grid gap-4 lg:grid-cols-2">
            <ChartCard title="Risk Distribution">
              <ChartShell isLoading={risk.isLoading}>
                {risk.data && <RiskDistributionChart data={risk.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Department Risk">
              <ChartShell isLoading={deptRisk.isLoading}>
                {deptRisk.data && <StackedRiskChart data={deptRisk.data} />}
              </ChartShell>
            </ChartCard>
            <ChartCard title="Top Risk Factors">
              <ChartShell isLoading={riskFactors.isLoading}>
                {riskFactors.data && <RiskFactorChart data={riskFactors.data} />}
              </ChartShell>
            </ChartCard>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
