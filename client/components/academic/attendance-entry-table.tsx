"use client";

import { useEffect, useMemo, useState } from "react";
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
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import type { AttendanceRoster } from "@/hooks/use-academic-entry";
import { showErrorToast, showSuccessToast } from "@/lib/toast";

interface AttendanceEntryTableProps {
  roster: AttendanceRoster | undefined;
  isLoading: boolean;
  hasApplied?: boolean;
  showRange?: boolean;
  canEdit?: boolean;
  onSave: (entries: { enrollment_id: string; attendance_percentage: number }[]) => Promise<void>;
  isSaving?: boolean;
}

export function AttendanceEntryTable({
  roster,
  isLoading,
  hasApplied = true,
  showRange = false,
  canEdit = true,
  onSave,
  isSaving,
}: AttendanceEntryTableProps) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [dirty, setDirty] = useState(false);

  const initialValues = useMemo(() => {
    if (!roster) return {};
    const init: Record<string, string> = {};
    for (const s of roster.students) {
      if (!s.enrollment_id) continue;
      init[s.enrollment_id] =
        s.attendance_percentage != null ? String(s.attendance_percentage) : "";
    }
    return init;
  }, [roster]);

  useEffect(() => {
    setValues(initialValues);
    setErrors({});
    setDirty(false);
  }, [initialValues]);

  function validate(raw: string): string | null {
    if (raw === "") return null;
    const num = parseFloat(raw);
    if (Number.isNaN(num)) return "Invalid";
    if (num < 0 || num > 100) return "0–100";
    return null;
  }

  function handleChange(enrollmentId: string, raw: string) {
    setValues((prev) => ({ ...prev, [enrollmentId]: raw }));
    setDirty(true);
    const err = validate(raw);
    setErrors((prev) => {
      const next = { ...prev };
      if (err) next[enrollmentId] = err;
      else delete next[enrollmentId];
      return next;
    });
  }

  async function handleSave() {
    if (!roster) return;
    const newErrors: Record<string, string> = {};
    const entries: { enrollment_id: string; attendance_percentage: number }[] = [];

    for (const s of roster.students) {
      if (!s.enrollment_id) continue;
      const raw = values[s.enrollment_id] ?? "";
      const initial = initialValues[s.enrollment_id] ?? "";
      if (raw === initial) continue;
      const err = validate(raw);
      if (err) {
        newErrors[s.enrollment_id] = err;
        continue;
      }
      if (raw !== "") {
        entries.push({
          enrollment_id: s.enrollment_id,
          attendance_percentage: parseFloat(raw),
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
      showSuccessToast({ description: `Updated ${entries.length} attendance records.` });
      setDirty(false);
    } catch {
      // handled by mutation
    }
  }

  if (isLoading) {
    return <p className="text-sm text-muted-foreground">Loading attendance roster…</p>;
  }
  if (!hasApplied || !roster) {
    return (
      <p className="text-sm text-muted-foreground">
        Select filters and apply to load the attendance table.
      </p>
    );
  }

  if (roster.students.length === 0) {
    return (
      <div className="rounded-lg border border-dashed p-6 text-sm">
        <p className="font-medium">No attendance records found for this selection.</p>
        <p className="mt-1 text-muted-foreground">
          Try changing the date range or academic filters.
        </p>
      </div>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-base">
            {roster.course_code
              ? `${roster.course_code} — ${roster.course_name}`
              : "All matching courses"}
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {roster.students.length} students
            {showRange ? " · counts are for the selected dates" : ""}
            {dirty ? " · Unsaved changes" : ""}
            {!canEdit ? " · select a course to edit overall attendance %" : ""}
          </p>
        </div>
        {canEdit && (
          <Button onClick={handleSave} disabled={isSaving || !dirty}>
            Save Attendance
          </Button>
        )}
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableSerialHead />
              <TableHead>Student</TableHead>
              <TableHead>Register No</TableHead>
              <TableHead>Section</TableHead>
              <TableHead>Overall %</TableHead>
              {showRange && (
                <>
                  <TableHead>Present</TableHead>
                  <TableHead>Absent</TableHead>
                  <TableHead>In selected dates</TableHead>
                </>
              )}
            </TableRow>
          </TableHeader>
          <TableBody>
            {roster.students.map((s, index) => {
              const key = s.enrollment_id ?? s.student_id;
              const err = s.enrollment_id ? errors[s.enrollment_id] : undefined;
              return (
                <TableRow key={key}>
                  <TableSerialCell index={index} />
                  <TableCell>{s.student_name}</TableCell>
                  <TableCell>{s.roll_number}</TableCell>
                  <TableCell>{s.section ?? "—"}</TableCell>
                  <TableCell>
                    {canEdit && s.enrollment_id ? (
                      <Input
                        type="number"
                        min={0}
                        max={100}
                        className={`w-24 ${err ? "border-destructive" : ""}`}
                        value={values[s.enrollment_id] ?? ""}
                        onChange={(e) =>
                          handleChange(s.enrollment_id as string, e.target.value)
                        }
                        title={err ?? "Stored enrollment percentage"}
                      />
                    ) : (
                      <span className="text-muted-foreground">
                        {s.attendance_percentage ?? "—"}
                      </span>
                    )}
                  </TableCell>
                  {showRange && (
                    <>
                      <TableCell>{s.range_present ?? "—"}</TableCell>
                      <TableCell>{s.range_absent ?? "—"}</TableCell>
                      <TableCell>
                        {s.range_percentage != null ? `${s.range_percentage}%` : "—"}
                      </TableCell>
                    </>
                  )}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
