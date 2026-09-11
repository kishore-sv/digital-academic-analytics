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
  onSave: (entries: { enrollment_id: string; attendance_percentage: number }[]) => Promise<void>;
  isSaving?: boolean;
}

export function AttendanceEntryTable({
  roster,
  isLoading,
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
  if (!roster) {
    return (
      <p className="text-sm text-muted-foreground">
        Select filters and apply to load the attendance table.
      </p>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-base">
            {roster.course_code} — {roster.course_name}
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {roster.students.length} students{dirty ? " · Unsaved changes" : ""}
          </p>
        </div>
        <Button onClick={handleSave} disabled={isSaving || !dirty}>Save Attendance</Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableSerialHead />
              <TableHead>Student</TableHead>
              <TableHead>Register No</TableHead>
              <TableHead>Section</TableHead>
              <TableHead>Attendance %</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {roster.students.map((s, index) => {
              const err = errors[s.enrollment_id];
              return (
                <TableRow key={s.enrollment_id}>
                  <TableSerialCell index={index} />
                  <TableCell>{s.student_name}</TableCell>
                  <TableCell>{s.roll_number}</TableCell>
                  <TableCell>{s.section ?? "—"}</TableCell>
                  <TableCell>
                    <Input
                      type="number"
                      min={0}
                      max={100}
                      className={`w-24 ${err ? "border-destructive" : ""}`}
                      value={values[s.enrollment_id] ?? ""}
                      onChange={(e) => handleChange(s.enrollment_id, e.target.value)}
                      title={err ?? undefined}
                    />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
