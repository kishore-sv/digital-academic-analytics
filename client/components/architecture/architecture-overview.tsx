import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { VerticalFlow } from "@/components/architecture/vertical-flow";

const STACK = [
  { name: "PostgreSQL", category: "Database" },
  { name: "SQLAlchemy ORM", category: "ORM" },
  { name: "Alembic", category: "Migrations" },
  { name: "FastAPI", category: "Backend" },
  { name: "Next.js", category: "Frontend" },
] as const;

const META = [
  { label: "Architecture type", value: "Modular monolith" },
  { label: "Database", value: "PostgreSQL" },
  { label: "ORM", value: "SQLAlchemy" },
  { label: "Migrations", value: "Alembic" },
  { label: "Backend", value: "FastAPI" },
  { label: "Frontend", value: "Next.js (App Router)" },
] as const;

export function ArchitectureOverview() {
  return (
    <div className="grid gap-8 lg:grid-cols-2">
      <div className="space-y-6">
        <div>
          <h2 className="text-lg font-semibold">Stack overview</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Technologies present in this repository today.
          </p>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          {STACK.map((item) => (
            <Card key={item.name} size="sm">
              <CardHeader className="pb-1">
                <CardTitle className="text-base">{item.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-xs text-muted-foreground">{item.category}</p>
              </CardContent>
            </Card>
          ))}
        </div>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">System metadata</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2 sm:grid-cols-2">
            {META.map((row) => (
              <div key={row.label} className="rounded-md border border-border/60 px-3 py-2">
                <p className="text-xs text-muted-foreground">{row.label}</p>
                <p className="text-sm font-medium">{row.value}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">End-to-end flow</h2>
        <VerticalFlow
          steps={[
            { label: "Next.js frontend", accent: "ui" },
            { label: "FastAPI backend", accent: "default" },
            { label: "SQLAlchemy ORM", accent: "default" },
            { label: "PostgreSQL", accent: "db" },
            { label: "Academic data", sublabel: "Marks, attendance, results", accent: "db" },
            { label: "Feature preparation", accent: "ml" },
            { label: "ML models & risk engine", accent: "ml" },
            { label: "Dashboards & reports", accent: "ui" },
          ]}
        />
      </div>
    </div>
  );
}
