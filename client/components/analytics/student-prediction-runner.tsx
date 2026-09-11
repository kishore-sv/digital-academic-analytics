"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PredictionCard } from "@/components/analytics/prediction-card";
import { usePredictForStudent } from "@/hooks/use-predictions";
import { useStudents, type Student } from "@/hooks/use-students";

interface StudentPredictionRunnerProps {
  title?: string;
  description?: string;
}

export function StudentPredictionRunner({
  title = "Run Student Prediction",
  description = "Select a student to run ML predictions using their academic data.",
}: StudentPredictionRunnerProps) {
  const { data, isLoading } = useStudents();
  const students = data?.data ?? [];
  const studentItems = students.map((student) => ({
    value: student.id,
    label: `${student.roll_number} — ${student.name}`,
  }));
  const [studentId, setStudentId] = useState<string>("");
  const { mutate, data: prediction, isPending, error } = usePredictForStudent();

  const selected = students.find((s) => s.id === studentId);

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      {isLoading && <LoadingState />}
      {!isLoading && students.length === 0 && (
        <EmptyState title="No students available" />
      )}
      {students.length > 0 && (
        <div className="flex flex-wrap items-end gap-3">
          <div className="min-w-[240px] space-y-1">
            <Label>Student</Label>
            <Select
              items={studentItems}
              value={studentId}
              onValueChange={(v) => setStudentId(v ?? "")}
            >
              <SelectTrigger className="w-auto min-w-72 max-w-96">
                <SelectValue placeholder="Select student" />
              </SelectTrigger>
              <SelectContent>
                {students.map((student: Student) => (
                  <SelectItem key={student.id} value={student.id}>
                    {student.roll_number} — {student.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <Button
            onClick={() => studentId && mutate(studentId)}
            disabled={!studentId || isPending}
          >
            {isPending ? "Predicting..." : "Run Prediction"}
          </Button>
        </div>
      )}
      {selected && (
        <p className="text-sm text-muted-foreground">
          {selected.name} · {selected.branch} · Semester {selected.semester}
        </p>
      )}
      {error && <ErrorState description="Prediction failed for selected student." />}
      {prediction && <PredictionCard predictions={prediction} />}
    </div>
  );
}
