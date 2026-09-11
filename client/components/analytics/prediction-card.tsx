import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { RiskBadge } from "@/components/analytics/risk-badge";
import type { AllPredictions } from "@/types/prediction";

interface PredictionCardProps {
  predictions: AllPredictions;
}

export function PredictionCard({ predictions }: PredictionCardProps) {
  const { performance, pass_fail, risk } = predictions;

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Predicted End-Term Performance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">
            {Math.round(performance.predicted_end_marks)} / 100
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            ML-powered academic prediction
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Likelihood of Passing
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-3xl font-bold">
            {Math.round(pass_fail.pass_probability * 100)}%
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Predicted: {pass_fail.prediction}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Academic Risk
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <RiskBadge level={risk.risk_level} />
            <span className="text-2xl font-bold">{risk.risk_score}</span>
          </div>
          {risk.risk_factors.length > 0 && (
            <ul className="text-xs text-muted-foreground mt-2 space-y-1">
              {risk.risk_factors.slice(0, 3).map((f) => (
                <li key={f}>• {f}</li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
