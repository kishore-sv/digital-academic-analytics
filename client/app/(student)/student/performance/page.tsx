"use client";

import { useState } from "react";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { StatCard } from "@/components/analytics/stat-card";
import { PerformanceTrendChart } from "@/components/analytics/charts/performance-trend-chart";
import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useStudentPerformance } from "@/hooks/use-student-performance";
import { usePerformanceTrends } from "@/hooks/use-analytics";

export default function StudentPerformancePage() {
  const { data, isLoading, error } = useStudentPerformance();
  const { data: trends } = usePerformanceTrends();
  const [selectedSemIdx, setSelectedSemIdx] = useState(0);

  const semesters = data?.semesters ?? [];
  const selectedSem = semesters[selectedSemIdx];
  const semesterItems = semesters.map((s) => ({
    value: String(s.semester_number),
    label: s.semester_name,
  }));

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState description="Unable to load performance data." />;
  if (!data || semesters.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="My Performance"
          description="Semester-wise academic results and analytics."
        />
        <EmptyState title="No performance data" description="Academic records are not yet available." />
      </div>
    );
  }

  const trendData =
    trends ??
    semesters.map((s) => ({
      semester: s.semester_name,
      average_sgpa: s.sgpa,
      average_cgpa: s.cgpa,
      pass_percentage: null,
    }));

  return (
    <div className="space-y-6">
      <PageHeader
        title="My Performance"
        description="Semester-wise academic results, trends, and course breakdown."
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Current CGPA" value={data.current_cgpa?.toFixed(2) ?? "—"} />
        <StatCard title="Current SGPA" value={data.current_sgpa?.toFixed(2) ?? "—"} />
        <StatCard title="Total Credits" value={String(data.total_credits)} />
        <StatCard title="Backlogs" value={String(data.backlogs)} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">CGPA / SGPA Trend</CardTitle>
        </CardHeader>
        <CardContent>
          <PerformanceTrendChart data={trendData} />
        </CardContent>
      </Card>

      <div className="flex flex-wrap items-center gap-3">
        <Select
          items={semesterItems}
          value={String(selectedSem?.semester_number ?? "")}
          onValueChange={(v) => {
            const idx = semesters.findIndex((s) => String(s.semester_number) === v);
            if (idx >= 0) setSelectedSemIdx(idx);
          }}
        >
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Select semester" />
          </SelectTrigger>
          <SelectContent>
            {semesters.map((s) => (
              <SelectItem key={s.semester_id} value={String(s.semester_number)}>
                {s.semester_name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {selectedSem && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard title="SGPA" value={selectedSem.sgpa?.toFixed(2) ?? "—"} />
            <StatCard title="CGPA" value={selectedSem.cgpa?.toFixed(2) ?? "—"} />
            <StatCard
              title="Passed"
              value={`${selectedSem.passed_courses} / ${selectedSem.passed_courses + selectedSem.failed_courses}`}
            />
            <StatCard
              title="Avg Attendance"
              value={
                selectedSem.average_attendance != null
                  ? `${selectedSem.average_attendance.toFixed(1)}%`
                  : "—"
              }
            />
          </div>

          {(selectedSem.strongest_course || selectedSem.weakest_course) && (
            <div className="grid gap-4 sm:grid-cols-2">
              {selectedSem.strongest_course && (
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-sm text-muted-foreground">Strongest</p>
                    <p className="font-medium">{selectedSem.strongest_course}</p>
                  </CardContent>
                </Card>
              )}
              {selectedSem.weakest_course && (
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-sm text-muted-foreground">Needs improvement</p>
                    <p className="font-medium">{selectedSem.weakest_course}</p>
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                {selectedSem.semester_name} — Course Results
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Course</TableHead>
                    <TableHead>Credits</TableHead>
                    <TableHead>Marks</TableHead>
                    <TableHead>Grade</TableHead>
                    <TableHead>GP</TableHead>
                    <TableHead>Attendance</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {selectedSem.courses.map((c) => (
                    <TableRow key={c.course_id}>
                      <TableCell>{c.course_name}</TableCell>
                      <TableCell>{c.credits}</TableCell>
                      <TableCell>{c.marks?.toFixed(1) ?? "—"}</TableCell>
                      <TableCell>{c.grade ?? "—"}</TableCell>
                      <TableCell>{c.grade_point?.toFixed(1) ?? "—"}</TableCell>
                      <TableCell>
                        {c.attendance_percentage != null
                          ? `${c.attendance_percentage.toFixed(1)}%`
                          : "—"}
                      </TableCell>
                      <TableCell>
                        <span
                          className={
                            c.status === "PASS"
                              ? "text-green-600 dark:text-green-400"
                              : c.status === "FAIL"
                                ? "text-red-600 dark:text-red-400"
                                : ""
                          }
                        >
                          {c.status ?? "—"}
                        </span>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
