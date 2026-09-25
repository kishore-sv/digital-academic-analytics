import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { VerticalFlow } from "@/components/architecture/vertical-flow";

export function DataFlowDiagram() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Academic data flow</CardTitle>
        <p className="text-sm text-muted-foreground">
          From day-to-day entry through analytics surfaces in the app.
        </p>
      </CardHeader>
      <CardContent>
        <VerticalFlow
          steps={[
            { label: "Academic data entry", sublabel: "Admin & faculty portals" },
            { label: "Marks & attendance", sublabel: "assessment_marks, attendances, enrollments" },
            { label: "PostgreSQL", accent: "db" },
            { label: "Results & semester aggregates", sublabel: "course_results, semester_results" },
            { label: "Feature preparation", sublabel: "feature_preparation service", accent: "ml" },
            { label: "ML models & risk engine", accent: "ml" },
            { label: "Predictions & risk assessment", sublabel: "prediction_results" },
            { label: "Analytics APIs", accent: "default" },
            { label: "Dashboards", accent: "ui" },
            { label: "Reports", sublabel: "PDF/HTML generation", accent: "ui" },
          ]}
        />
      </CardContent>
    </Card>
  );
}
