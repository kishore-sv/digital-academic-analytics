import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { VerticalFlow } from "@/components/architecture/vertical-flow";

export function MultiTenancyDiagram() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold">Multi-tenancy</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Shared PostgreSQL database with <strong className="font-medium">row-level</strong>{" "}
          isolation: tenant-owned tables include <code className="text-xs">institution_id</code>.
          This is <em>not</em> database-per-tenant or schema-per-tenant.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Conceptual tenant-isolation view</CardTitle>
          <p className="text-sm text-muted-foreground">
            Illustrative only — generic institution names.
          </p>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center gap-4 text-center">
            <div className="rounded-lg border border-blue-200/80 bg-blue-50/80 px-6 py-3 dark:border-blue-900 dark:bg-blue-950/40">
              <p className="font-medium">PostgreSQL (single database)</p>
            </div>
            <p className="text-muted-foreground">↓</p>
            <div className="grid w-full max-w-2xl gap-4 sm:grid-cols-2">
              <div className="rounded-lg border bg-card p-4 shadow-sm">
                <p className="font-semibold">Institution A</p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Students, faculty, courses, marks, results — all rows tagged with
                  institution A&apos;s <code>institution_id</code>
                </p>
              </div>
              <div className="rounded-lg border bg-card p-4 shadow-sm">
                <p className="font-semibold">Institution B</p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Separate academic data with institution B&apos;s{" "}
                  <code>institution_id</code>; never mixed in API queries
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Request scoping flow</CardTitle>
        </CardHeader>
        <CardContent>
          <VerticalFlow
            compact
            steps={[
              { label: "Tenant context", sublabel: "institution_id on User + JWT payload" },
              { label: "Authentication", sublabel: "Login + httpOnly cookies" },
              { label: "User role", sublabel: "institution_admin | faculty | student | parent" },
              { label: "Institution scope", sublabel: "Filter queries by institution_id" },
              { label: "Authorized data", sublabel: "Role-based student/resource filters" },
            ]}
          />
          <p className="mt-4 text-sm text-muted-foreground">
            Backend authorization and tenant helpers (e.g.{" "}
            <code className="text-xs">get_tenant_entity</code>,{" "}
            <code className="text-xs">get_accessible_student_ids</code>) prevent cross-institution
            access. Users cannot read another institution&apos;s rows even if they guess UUIDs.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
