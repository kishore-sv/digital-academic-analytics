"use client";

import { StudentPredictionRunner } from "@/components/analytics/student-prediction-runner";
import { PageHeader } from "@/components/layout/page-header";

export default function FacultyPredictionsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Student Predictions"
        description="Run ML predictions for your assigned students."
      />
      <StudentPredictionRunner />
    </div>
  );
}
