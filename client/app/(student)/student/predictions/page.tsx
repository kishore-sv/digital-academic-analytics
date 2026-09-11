"use client";

import { Button } from "@/components/ui/button";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PredictionCard } from "@/components/analytics/prediction-card";
import { PageHeader } from "@/components/layout/page-header";
import { useMyStudentProfile } from "@/hooks/use-students";
import { usePredictForStudent } from "@/hooks/use-predictions";

export default function StudentPredictionsPage() {
  const { data: student } = useMyStudentProfile();
  const { mutate, data, isPending, error } = usePredictForStudent();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Your Predictions"
        description="ML-powered end-term performance, pass likelihood, and academic risk."
      />
      <Button
        onClick={() => student && mutate(student.id)}
        disabled={!student || isPending}
      >
        {isPending ? "Generating..." : "Generate Prediction"}
      </Button>
      {isPending && <LoadingState />}
      {error && <ErrorState description="Could not generate prediction." />}
      {data && <PredictionCard predictions={data} />}
    </div>
  );
}
