"use client";

import { CGPADistributionChart } from "@/components/analytics/charts/cgpa-distribution-chart";
import { PerformanceTrendChart } from "@/components/analytics/charts/performance-trend-chart";
import { PassFailChart } from "@/components/analytics/charts/pass-fail-chart";
import { PredictionDistributionChart } from "@/components/analytics/charts/prediction-distribution-chart";
import { RiskFactorChart } from "@/components/analytics/charts/risk-factor-chart";
import { StackedRiskChart } from "@/components/analytics/charts/stacked-risk-chart";
import { DepartmentPerformanceChart } from "@/components/analytics/department-performance-chart";
import { ReportAtRiskTable } from "@/components/analytics/report-at-risk-table";
import { RiskDistributionChart } from "@/components/analytics/risk-distribution-chart";
import { StatCard } from "@/components/analytics/stat-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { ReportContext } from "@/types/report";

export function ReportPreview({ data }: { data: ReportContext }) {
  const { header, kpis } = data;
  const overview = kpis.overview;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">{header.institution_name}</CardTitle>
          <p className="text-sm text-muted-foreground">{header.title}</p>
        </CardHeader>
        <CardContent className="grid gap-1 text-sm text-muted-foreground sm:grid-cols-2">
          <p>Academic Year: {header.filters.academic_year}</p>
          <p>Semester: {header.filters.semester}</p>
          <p>Department: {header.filters.department}</p>
          <p>Program: {header.filters.program}</p>
          <p>Course: {header.filters.course}</p>
          <p>Risk Level: {header.filters.risk_level}</p>
          <p className="sm:col-span-2">
            Generated: {new Date(header.generated_at).toLocaleString()}
          </p>
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Students" value={overview.total_students} />
        <StatCard title="Avg CGPA" value={overview.average_cgpa.toFixed(2)} />
        <StatCard title="Avg SGPA" value={overview.average_sgpa.toFixed(2)} />
        <StatCard title="Pass %" value={`${overview.pass_percentage}%`} />
        <StatCard title="Fail %" value={`${kpis.fail_percentage}%`} />
        <StatCard title="At-Risk %" value={`${overview.at_risk_percentage}%`} />
        <StatCard title="High Risk" value={overview.high_risk_count} />
        <StatCard title="Avg Attendance" value={`${kpis.average_attendance}%`} />
        <StatCard title="Avg Predicted Marks" value={kpis.average_predicted_marks.toFixed(1)} />
        <StatCard title="Avg Pass Probability" value={`${kpis.average_pass_probability}%`} />
        <StatCard title="Avg Risk Score" value={kpis.average_risk_score.toFixed(1)} />
      </div>

      {data.findings.length > 0 && (
        <Card>
          <CardHeader><CardTitle className="text-base">Key Findings</CardTitle></CardHeader>
          <CardContent>
            <ul className="list-disc space-y-1 pl-5 text-sm">
              {data.findings.map((finding) => <li key={finding}>{finding}</li>)}
            </ul>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader><CardTitle className="text-base">CGPA Distribution</CardTitle></CardHeader>
          <CardContent><CGPADistributionChart data={data.cgpa_distribution} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">SGPA Distribution</CardTitle></CardHeader>
          <CardContent><CGPADistributionChart data={data.sgpa_distribution} /></CardContent>
        </Card>
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle className="text-base">Performance Trend</CardTitle></CardHeader>
          <CardContent>
            <PerformanceTrendChart data={data.performance_trends} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Department Performance</CardTitle></CardHeader>
          <CardContent>
            <DepartmentPerformanceChart departments={data.department_analytics} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Pass / Fail Trend</CardTitle></CardHeader>
          <CardContent><PassFailChart data={data.pass_fail_trend} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Risk Distribution</CardTitle></CardHeader>
          <CardContent><RiskDistributionChart data={data.risk_distribution} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Department Risk</CardTitle></CardHeader>
          <CardContent><StackedRiskChart data={data.department_risk_stacks} /></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Predicted Marks Distribution</CardTitle></CardHeader>
          <CardContent>
            <PredictionDistributionChart data={data.prediction_performance.distribution} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-base">Risk Factors</CardTitle></CardHeader>
          <CardContent><RiskFactorChart data={data.risk_factors} /></CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">At-Risk Students</CardTitle>
          <p className="text-sm text-muted-foreground">
            {data.at_risk_students.length} student(s) in selected scope
          </p>
        </CardHeader>
        <CardContent>
          {data.at_risk_students.length === 0 ? (
            <p className="text-sm text-muted-foreground">No students match the selected filters.</p>
          ) : (
            <ReportAtRiskTable students={data.at_risk_students} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
