"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { AnalyticsFiltersBar } from "@/components/analytics/analytics-filters";
import {
  AtRiskTableFiltersBar,
  type AtRiskTableFilters,
} from "@/components/analytics/at-risk-table-filters";
import { RiskBadge } from "@/components/analytics/risk-badge";
import { TrendBadge } from "@/components/analytics/trend-badge";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { RiskFactorChart } from "@/components/analytics/charts/risk-factor-chart";
import { StackedRiskChart } from "@/components/analytics/charts/stacked-risk-chart";
import { ChartShell } from "@/components/analytics/charts/chart-shell";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useAtRiskStudents, useDepartments } from "@/hooks/use-academic";
import {
  useAtRiskSummary,
  useDepartmentRiskStacks,
  useRiskDistribution,
} from "@/hooks/use-analytics";
import type { AnalyticsFilters } from "@/types/analytics";
import { ROUTES } from "@/lib/constants";
import {
  serialStart,
  TableSerialCell,
  TableSerialHead,
} from "@/components/layout/table-serial";

export default function AdminAtRiskPage() {
  const [chartFilters, setChartFilters] = useState<AnalyticsFilters>({});
  const [tableFilters, setTableFilters] = useState<AtRiskTableFilters>({});
  const [page, setPage] = useState(1);

  const pageSize = 50;
  const { data, isLoading, error } = useAtRiskStudents(page, pageSize, tableFilters);
  const summary = useAtRiskSummary(chartFilters);
  const risk = useRiskDistribution(chartFilters);
  const deptRisk = useDepartmentRiskStacks(chartFilters);

  const { data: deptData } = useDepartments();
  const students = data?.data ?? [];
  const meta = data?.meta;

  const departments = useMemo(
    () => (deptData?.data ?? []).map((d) => d.name).sort(),
    [deptData],
  );
  const semesters = useMemo(() => Array.from({ length: 8 }, (_, i) => i + 1), []);

  function handleTableFiltersChange(next: AtRiskTableFilters) {
    setTableFilters(next);
    setPage(1);
  }

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <h1 className="text-2xl font-semibold tracking-tight">At-Risk Students</h1>
        <p className="text-muted-foreground">
          Students flagged with medium or high academic risk.
        </p>
        <AnalyticsFiltersBar value={chartFilters} onChange={setChartFilters} />
      </div>

      {summary.data && (
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard title="Low Risk" value={summary.data.low} />
          <StatCard title="Medium Risk" value={summary.data.medium} />
          <StatCard title="High Risk" value={summary.data.high} />
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-3">
        <Card>
          <CardHeader><CardTitle className="text-base">Risk Distribution</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isLoading={risk.isLoading}>
              {risk.data && <RiskDistributionChart data={risk.data} />}
            </ChartShell>
          </CardContent>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle className="text-base">Department Risk</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isLoading={deptRisk.isLoading}>
              {deptRisk.data && <StackedRiskChart data={deptRisk.data} />}
            </ChartShell>
          </CardContent>
        </Card>
        <Card className="lg:col-span-3">
          <CardHeader><CardTitle className="text-base">Risk Factors</CardTitle></CardHeader>
          <CardContent>
            <ChartShell isLoading={summary.isLoading}>
              {summary.data?.risk_factors && (
                <RiskFactorChart data={summary.data.risk_factors} />
              )}
            </ChartShell>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold">At-Risk Roster</h2>
          {meta && (
            <p className="text-sm text-muted-foreground">
              Showing {students.length} of {meta.total} at-risk students
            </p>
          )}
        </div>

        <AtRiskTableFiltersBar
          value={tableFilters}
          onChange={handleTableFiltersChange}
          departments={departments}
          semesters={semesters}
        />

        {isLoading && <LoadingState />}
        {error && <ErrorState description="Unable to load at-risk students." />}
        {!isLoading && !error && students.length === 0 && (
          <EmptyState
            title="No at-risk students"
            description="Try adjusting filters or wait for ML predictions to populate."
          />
        )}

        {!isLoading && !error && students.length > 0 && (
        <Table>
          <TableHeader>
            <TableRow>
              <TableSerialHead />
              <TableHead>Roll No</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Semester</TableHead>
              <TableHead>Risk</TableHead>
              <TableHead>Score</TableHead>
              <TableHead>Attendance</TableHead>
              <TableHead>CGPA</TableHead>
              <TableHead>Trend</TableHead>
              <TableHead />
            </TableRow>
          </TableHeader>
          <TableBody>
            {students.map((s, index) => (
              <TableRow key={s.student_id}>
                <TableSerialCell index={index} start={serialStart(page, pageSize)} />
                <TableCell>{s.roll_number}</TableCell>
                <TableCell>{s.student_name}</TableCell>
                <TableCell>{s.department_name ?? "—"}</TableCell>
                <TableCell>{s.semester ?? "—"}</TableCell>
                <TableCell><RiskBadge level={s.risk_level} /></TableCell>
                <TableCell>{s.risk_score.toFixed(1)}</TableCell>
                <TableCell>
                  {s.attendance_percentage != null
                    ? `${s.attendance_percentage.toFixed(0)}%`
                    : "—"}
                </TableCell>
                <TableCell>{s.cgpa?.toFixed(2) ?? "—"}</TableCell>
                <TableCell>
                  {s.performance_trend ? (
                    <TrendBadge trend={s.performance_trend} />
                  ) : (
                    "—"
                  )}
                </TableCell>
                <TableCell>
                  <Link
                    href={ROUTES.admin.predictions}
                    className="text-sm text-primary hover:underline"
                  >
                    View
                  </Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        )}

        {meta && meta.total_pages > 1 && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">
              Page {meta.page} of {meta.total_pages}
            </span>
            <div className="flex gap-2">
              <button
                type="button"
                className="rounded-md border px-3 py-1 disabled:opacity-50"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Previous
              </button>
              <button
                type="button"
                className="rounded-md border px-3 py-1 disabled:opacity-50"
                disabled={page >= meta.total_pages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
