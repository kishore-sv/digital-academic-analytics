"use client";

import { useMemo, useState } from "react";
import { RiskBadge } from "@/components/analytics/risk-badge";
import { TrendBadge } from "@/components/analytics/trend-badge";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { AtRiskReportRow } from "@/types/report";

type SortKey = "student_name" | "roll_number" | "risk_score" | "cgpa" | "attendance_percentage";

export function ReportAtRiskTable({ students }: { students: AtRiskReportRow[] }) {
  const [sortKey, setSortKey] = useState<SortKey>("risk_score");
  const [asc, setAsc] = useState(false);

  const sorted = useMemo(() => {
    return [...students].sort((a, b) => {
      const av = a[sortKey] ?? "";
      const bv = b[sortKey] ?? "";
      if (typeof av === "number" && typeof bv === "number") {
        return asc ? av - bv : bv - av;
      }
      return asc
        ? String(av).localeCompare(String(bv))
        : String(bv).localeCompare(String(av));
    });
  }, [students, sortKey, asc]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) setAsc(!asc);
    else {
      setSortKey(key);
      setAsc(false);
    }
  }

  function head(label: string, key: SortKey) {
    return (
      <TableHead>
        <button type="button" className="font-medium hover:underline" onClick={() => toggleSort(key)}>
          {label}
        </button>
      </TableHead>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableSerialHead />
          {head("Name", "student_name")}
          {head("Roll No", "roll_number")}
          <TableHead>Department</TableHead>
          <TableHead>Program</TableHead>
          <TableHead>Semester</TableHead>
          {head("CGPA", "cgpa")}
          {head("Attendance", "attendance_percentage")}
          <TableHead>Backlogs</TableHead>
          {head("Risk Score", "risk_score")}
          <TableHead>Risk</TableHead>
          <TableHead>Trend</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {sorted.map((s, index) => (
          <TableRow key={s.student_id}>
            <TableSerialCell index={index} />
            <TableCell className="font-medium">{s.student_name}</TableCell>
            <TableCell className="font-mono text-sm">{s.roll_number}</TableCell>
            <TableCell>{s.department_name ?? "—"}</TableCell>
            <TableCell>{s.program_name ?? "—"}</TableCell>
            <TableCell>{s.semester ?? "—"}</TableCell>
            <TableCell>{s.cgpa?.toFixed(2) ?? "—"}</TableCell>
            <TableCell>
              {s.attendance_percentage != null ? `${s.attendance_percentage.toFixed(0)}%` : "—"}
            </TableCell>
            <TableCell>{s.backlog_count ?? "—"}</TableCell>
            <TableCell>{s.risk_score.toFixed(1)}</TableCell>
            <TableCell><RiskBadge level={s.risk_level} /></TableCell>
            <TableCell>
              {s.performance_trend ? <TrendBadge trend={s.performance_trend} /> : "—"}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
