import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const ROLES = [
  {
    role: "Institution Admin",
    code: "institution_admin",
    scope: "All students and academic data within the institution (institution_id scope).",
    enforced: true,
    note: "get_accessible_student_ids returns null → full institution student query.",
  },
  {
    role: "Faculty",
    code: "faculty",
    scope:
      "Students linked via faculty_students; marks entry may use faculty_courses when assigned to a course (all enrollments for that course) or mentored students otherwise.",
    enforced: true,
    note: "Implemented in authorization_service and marks_entry_service.",
  },
  {
    role: "Student",
    code: "student",
    scope: "Own student profile, enrollments, results, predictions, and goals only.",
    enforced: true,
    note: "Scoped to the Student row tied to the logged-in user.",
  },
  {
    role: "Parent",
    code: "parent",
    scope: "Linked children only (parent_students junction).",
    enforced: true,
    note: "get_linked_child_ids drives accessible student IDs.",
  },
] as const;

export function RoleAccessCards() {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-base font-semibold">Role-based data access</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Scopes reflect <code className="text-xs">authorization_service.py</code> as
          implemented today.
        </p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        {ROLES.map((item) => (
          <Card key={item.code} size="sm">
            <CardHeader className="gap-2">
              <div className="flex flex-wrap items-center gap-2">
                <CardTitle className="text-base">{item.role}</CardTitle>
                <Badge variant="secondary" className="font-mono text-[10px] font-normal">
                  {item.code}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <div>
                <p className="text-xs font-medium text-muted-foreground">Scope</p>
                <p>{item.scope}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground">Status</p>
                <p className="text-emerald-700 dark:text-emerald-400">
                  {item.enforced ? "Enforced in backend" : "Planned / in progress"}
                </p>
              </div>
              <p className="text-xs text-muted-foreground">{item.note}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
