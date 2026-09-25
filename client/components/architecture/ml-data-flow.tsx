import { RiskBadge } from "@/components/analytics/risk-badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  FEATURE_PREPARATION_FIELDS,
  ML_MODELS,
  RISK_ENGINE_FEATURES,
} from "@/lib/architecture/ml-pipeline-metadata";
import { VerticalFlow } from "@/components/architecture/vertical-flow";

export function MLDataFlow() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold">Database → ML pipeline</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          How relational academic data becomes model inputs and stored predictions.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Feature preparation</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <VerticalFlow
            compact
            steps={[
              { label: "Student academic records", accent: "db" },
              { label: "Enrollments + marks + semester results", accent: "db" },
              { label: "Feature vector (build_features_from_enrollment)", accent: "ml" },
              { label: "ML models & risk engine", accent: "ml" },
              { label: "prediction_results table", accent: "db" },
            ]}
          />
          <Separator />
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {FEATURE_PREPARATION_FIELDS.map((f) => (
              <div
                key={f.key}
                className="rounded-md border border-border/60 px-3 py-2 text-xs"
              >
                <p className="font-mono font-medium">{f.key}</p>
                <p className="text-muted-foreground">{f.label}</p>
                <p className="mt-0.5 text-[10px] text-muted-foreground">Source: {f.source}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-3">
        {ML_MODELS.map((model) => (
          <Card key={model.id} size="sm">
            <CardHeader>
              <CardTitle className="text-sm leading-snug">{model.name}</CardTitle>
              <p className="text-xs text-muted-foreground">{model.implementation}</p>
            </CardHeader>
            <CardContent className="space-y-2 text-xs">
              <p className="font-mono text-muted-foreground">{model.module}</p>
              <div>
                <p className="font-medium">Outputs</p>
                <ul className="mt-1 list-inside list-disc text-muted-foreground">
                  {model.outputs.map((o) => (
                    <li key={o}>{o}</li>
                  ))}
                </ul>
              </div>
              {model.id === "model3" && (
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <span className="text-muted-foreground">Risk levels:</span>
                  <RiskBadge level="LOW" />
                  <RiskBadge level="MEDIUM" />
                  <RiskBadge level="HIGH" />
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Model 3 inputs (risk engine)</CardTitle>
          <p className="text-sm text-muted-foreground">
            Rule-based weighted scoring — not a trained ML model.
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {RISK_ENGINE_FEATURES.map((key) => (
              <span
                key={key}
                className="rounded-md bg-muted px-2 py-1 font-mono text-xs"
              >
                {key}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
