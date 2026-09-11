"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { RecommendationList } from "@/components/analytics/recommendation-list";
import { RiskBadge } from "@/components/analytics/risk-badge";
import { PageHeader } from "@/components/layout/page-header";
import { useMyStudentPrediction } from "@/hooks/use-student-prediction";

export default function StudentImprovementPage() {
  const { data, isPending, error } = useMyStudentPrediction();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Improvement Guidance"
        description="Personalized recommendations based on your academic profile."
      />
      {isPending && <LoadingState />}
      {error && <ErrorState description="Unable to load improvement guidance." />}
      {data && (
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Academic Risk</CardTitle>
            </CardHeader>
            <CardContent className="flex items-center gap-3">
              <RiskBadge level={data.risk.risk_level} />
              <span className="text-2xl font-bold">{data.risk.risk_score}</span>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Risk Factors</CardTitle>
            </CardHeader>
            <CardContent>
              <RecommendationList title="" items={data.risk.risk_factors} />
            </CardContent>
          </Card>
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="text-base">Recommendations</CardTitle>
            </CardHeader>
            <CardContent>
              <RecommendationList title="" items={data.risk.recommendations} />
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
