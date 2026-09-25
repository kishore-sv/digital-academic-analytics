import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { VerticalFlow } from "@/components/architecture/vertical-flow";
import { RoleAccessCards } from "@/components/architecture/role-access-cards";

const PRINCIPLES = [
  {
    title: "Authentication",
    body: "Login via POST /api/v1/auth/login; passwords verified with Argon2 (argon2-cffi).",
  },
  {
    title: "Session tokens",
    body: "JWT access & refresh tokens stored in httpOnly cookies (not localStorage).",
  },
  {
    title: "Authorization",
    body: "Role checks on routes; student-level scope via authorization_service.",
  },
  {
    title: "Tenant isolation",
    body: "institution_id on tenant tables; queries filtered to the authenticated institution.",
  },
  {
    title: "Backend-enforced access",
    body: "assert_student_access / get_tenant_entity — UI is not the security boundary.",
  },
  {
    title: "Protected academic data",
    body: "Marks, attendance, results, and predictions require an authenticated session.",
  },
] as const;

export function SecurityFlow() {
  return (
    <div className="space-y-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Security & access flow</CardTitle>
        </CardHeader>
        <CardContent>
          <VerticalFlow
            compact
            steps={[
              { label: "Login" },
              { label: "Authentication", sublabel: "Argon2 password verify" },
              { label: "JWT in httpOnly cookies", sublabel: "access_token + refresh_token" },
              { label: "Role verification", sublabel: "institution_admin, faculty, student, parent" },
              { label: "Institution / tenant scope", sublabel: "institution_id from token + user" },
              { label: "Resource authorization", sublabel: "Student/course scope helpers" },
              { label: "Database query", sublabel: "SQLAlchemy with institution_id filters" },
            ]}
          />
        </CardContent>
      </Card>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {PRINCIPLES.map((p) => (
          <Card key={p.title} size="sm">
            <CardHeader>
              <CardTitle className="text-sm">{p.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground">{p.body}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <RoleAccessCards />
    </div>
  );
}
