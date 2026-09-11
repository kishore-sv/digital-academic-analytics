import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { TrendBadge } from "@/components/analytics/trend-badge";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import type { SemesterResult } from "@/hooks/use-academic";
import { cn } from "@/lib/utils";

interface SemesterResultsTableProps {
  results: SemesterResult[];
  highlightConcerns?: boolean;
}

function isConcerning(result: SemesterResult) {
  return (
    (result.backlog_count ?? 0) > 0 || result.performance_trend === "DECLINING"
  );
}

export function SemesterResultsTable({
  results,
  highlightConcerns = false,
}: SemesterResultsTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableSerialHead />
          <TableHead>Roll No</TableHead>
          <TableHead>Name</TableHead>
          <TableHead>SGPA</TableHead>
          <TableHead>CGPA</TableHead>
          <TableHead>Backlogs</TableHead>
          <TableHead>Trend</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {results.map((result, index) => (
          <TableRow
            key={result.id}
            className={cn(
              highlightConcerns &&
                isConcerning(result) &&
                "bg-amber-50/60 dark:bg-amber-950/20",
            )}
          >
            <TableSerialCell index={index} />
            <TableCell className="font-mono text-sm">
              {result.roll_number ?? "—"}
            </TableCell>
            <TableCell className="font-medium">
              {result.student_name ?? "—"}
            </TableCell>
            <TableCell>{result.sgpa?.toFixed(2) ?? "—"}</TableCell>
            <TableCell>{result.cgpa?.toFixed(2) ?? "—"}</TableCell>
            <TableCell
              className={cn(
                (result.backlog_count ?? 0) > 0 &&
                  "font-semibold text-red-600 dark:text-red-400",
              )}
            >
              {result.backlog_count}
            </TableCell>
            <TableCell>
              <TrendBadge trend={result.performance_trend} />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

export function semesterResultsSummary(results: SemesterResult[]) {
  const studentCount = new Set(results.map((r) => r.student_id)).size;
  const cgpaValues = results
    .map((r) => r.cgpa)
    .filter((v): v is number => v != null);
  const avgCgpa =
    cgpaValues.length > 0
      ? cgpaValues.reduce((sum, v) => sum + v, 0) / cgpaValues.length
      : null;
  const withBacklogs = results.filter((r) => (r.backlog_count ?? 0) > 0).length;
  const declining = results.filter(
    (r) => r.performance_trend === "DECLINING",
  ).length;

  return { studentCount, avgCgpa, withBacklogs, declining };
}
