"use client";

import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PredictionCard } from "@/components/analytics/prediction-card";
import { PageHeader } from "@/components/layout/page-header";
import { useStudent } from "@/hooks/use-students";
import { usePredictForStudent } from "@/hooks/use-predictions";
import { useReportDownloads } from "@/hooks/use-reports";

export default function FacultyStudentDetailPage() {
  const params = useParams();
  const studentId = params.id as string;
  const { data: student, isLoading, error } = useStudent(studentId);
  const { mutate, data: prediction, isPending } = usePredictForStudent();
  const { downloadStudentReport } = useReportDownloads();

  return (
    <div className="space-y-6">
      <PageHeader
        title={student?.name ?? "Student Detail"}
        description={student ? `${student.roll_number} · ${student.branch}` : undefined}
      />
      {isLoading && <LoadingState />}
      {error && <ErrorState description="Student not found or access denied." />}
      {student && (
        <div className="flex gap-2">
          <Button onClick={() => mutate(student.id)} disabled={isPending}>
            {isPending ? "Predicting..." : "Run Prediction"}
          </Button>
          <Button
            variant="outline"
            onClick={() => downloadStudentReport(student.id)}
          >
            Download Report
          </Button>
        </div>
      )}
      {prediction && <PredictionCard predictions={prediction} />}
    </div>
  );
}
