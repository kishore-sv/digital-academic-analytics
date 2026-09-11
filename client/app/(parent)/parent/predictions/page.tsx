"use client";

import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PredictionCard } from "@/components/analytics/prediction-card";
import { PageHeader } from "@/components/layout/page-header";
import { useMyStudentPrediction } from "@/hooks/use-student-prediction";

export default function ParentPredictionsPage() {
  const { data, isPending, error } = useMyStudentPrediction();

  return (
    <div className="space-y-6">
      <PageHeader title="Child Predictions" description="ML predictions for your linked child." />
      {isPending && <LoadingState />}
      {error && <ErrorState description="Unable to load predictions." />}
      {data && <PredictionCard predictions={data} />}
    </div>
  );
}
