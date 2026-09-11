"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { MarksGrid } from "@/hooks/use-academic-entry";
import { showErrorToast, showSuccessToast } from "@/lib/toast";

type CellKey = string;

function cellKey(enrollmentId: string, assessmentId: string): CellKey {
  return `${enrollmentId}:${assessmentId}`;
}

interface MarksEntryTableProps {
  grid: MarksGrid | undefined;
  isLoading: boolean;
  onSave: (entries: {
    enrollment_id: string;
    assessment_id: string;
    marks_obtained: number | null;
  }[]) => Promise<void>;
  onRegenerate?: () => void;
  isSaving?: boolean;
  isRegenerating?: boolean;
}

export function MarksEntryTable({
  grid,
  isLoading,
  onSave,
  onRegenerate,
  isSaving,
  isRegenerating,
}: MarksEntryTableProps) {
  const [values, setValues] = useState<Record<CellKey, string>>({});
  const [errors, setErrors] = useState<Record<CellKey, string>>({});
  const [dirty, setDirty] = useState(false);

  const initialValues = useMemo(() => {
    if (!grid) return {};
    const init: Record<CellKey, string> = {};
    for (const student of grid.students) {
      for (const mark of student.marks) {
        const key = cellKey(student.enrollment_id, mark.assessment_id);
        init[key] = mark.marks_obtained != null ? String(mark.marks_obtained) : "";
      }
    }
    return init;
  }, [grid]);

  useEffect(() => {
    setValues(initialValues);
    setErrors({});
    setDirty(false);
  }, [initialValues]);

  const validate = useCallback(
    (enrollmentId: string, assessmentId: string, raw: string): string | null => {
      if (raw === "") return null;
      const num = parseFloat(raw);
      if (Number.isNaN(num)) return "Invalid number";
      if (num < 0) return "Cannot be negative";
      const assessment = grid?.assessments.find((a) => a.id === assessmentId);
      if (assessment && num > assessment.max_marks) {
        return `Max ${assessment.max_marks}`;
      }
      return null;
    },
    [grid],
  );

  function handleChange(enrollmentId: string, assessmentId: string, raw: string) {
    const key = cellKey(enrollmentId, assessmentId);
    setValues((prev) => ({ ...prev, [key]: raw }));
    setDirty(true);
    const err = validate(enrollmentId, assessmentId, raw);
    setErrors((prev) => {
      const next = { ...prev };
      if (err) next[key] = err;
      else delete next[key];
      return next;
    });
  }

  function handleReset() {
    setValues(initialValues);
    setErrors({});
    setDirty(false);
  }

  async function handleSave() {
    if (!grid) return;
    const newErrors: Record<CellKey, string> = {};
    const entries: { enrollment_id: string; assessment_id: string; marks_obtained: number | null }[] = [];

    for (const student of grid.students) {
      for (const mark of student.marks) {
        const key = cellKey(student.enrollment_id, mark.assessment_id);
        const raw = values[key] ?? "";
        const initial = initialValues[key] ?? "";
        if (raw === initial) continue;

        const err = validate(student.enrollment_id, mark.assessment_id, raw);
        if (err) {
          newErrors[key] = err;
          continue;
        }
        entries.push({
          enrollment_id: student.enrollment_id,
          assessment_id: mark.assessment_id,
          marks_obtained: raw === "" ? null : parseFloat(raw),
        });
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      showErrorToast({ description: "Fix validation errors before saving." });
      return;
    }
    if (entries.length === 0) {
      showErrorToast({ description: "No changes to save." });
      return;
    }

    try {
      await onSave(entries);
      showSuccessToast({ description: `Saved ${entries.length} mark entries.` });
      setDirty(false);
    } catch {
      // handled by mutation
    }
  }

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">Loading marks roster…</p>;
  }

  if (!grid) {
    return (
      <p className="text-sm text-muted-foreground">
        Select filters and apply to load the marks table.
      </p>
    );
  }

  if (grid.students.length === 0) {
    return <p className="text-sm text-muted-foreground">No students match the selected filters.</p>;
  }

  return (
    <Card>
      <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
        <div>
          <CardTitle className="text-base">
            {grid.course_code} — {grid.course_name}
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {grid.course_type} · {grid.students.length} students
            {dirty && " · Unsaved changes"}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button onClick={handleSave} disabled={isSaving || !dirty}>
            Save Marks
          </Button>
          <Button variant="outline" onClick={handleReset} disabled={!dirty}>
            Reset Changes
          </Button>
          {onRegenerate && (
            <Button
              type="button"
              variant="outline"
              disabled={isRegenerating}
              onClick={onRegenerate}
            >
              Regenerate Predictions
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="sticky left-0 z-10 w-12 bg-background text-center">#</TableHead>
              <TableHead className="sticky left-12 z-10 min-w-36 bg-background">Student</TableHead>
              <TableHead className="sticky left-48 z-10 min-w-28 bg-background">Reg No</TableHead>
              {grid.assessments.map((a) => (
                <TableHead key={a.id} className="min-w-20 text-center">
                  <div className="text-xs font-normal text-muted-foreground">{a.assessment_type}</div>
                  {a.name}
                  <div className="text-xs font-normal">/{a.max_marks}</div>
                </TableHead>
              ))}
              <TableHead className="text-center">Total</TableHead>
              <TableHead className="text-center">Grade</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {grid.students.map((student, index) => (
              <TableRow key={student.enrollment_id}>
                <TableCell className="sticky left-0 z-10 w-12 bg-background text-center tabular-nums text-muted-foreground">
                  {index + 1}
                </TableCell>
                <TableCell className="sticky left-12 z-10 bg-background font-medium">
                  {student.student_name}
                </TableCell>
                <TableCell className="sticky left-48 z-10 bg-background">
                  {student.roll_number}
                </TableCell>
                {student.marks.map((mark) => {
                  const key = cellKey(student.enrollment_id, mark.assessment_id);
                  const err = errors[key];
                  return (
                    <TableCell key={mark.assessment_id} className="p-1">
                      <Input
                        type="number"
                        min={0}
                        step={0.5}
                        className={`h-8 w-20 text-center ${err ? "border-destructive" : ""}`}
                        value={values[key] ?? ""}
                        onChange={(e) =>
                          handleChange(student.enrollment_id, mark.assessment_id, e.target.value)
                        }
                        aria-invalid={!!err}
                        title={err ?? undefined}
                      />
                    </TableCell>
                  );
                })}
                <TableCell className="text-center text-sm">
                  {student.total_marks != null ? student.total_marks.toFixed(1) : "—"}
                </TableCell>
                <TableCell className="text-center text-sm font-medium">
                  {student.grade ?? "—"}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
