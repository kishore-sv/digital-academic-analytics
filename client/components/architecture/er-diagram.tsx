import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ERDiagramCanvas,
  type ERTreeNode,
} from "@/components/architecture/er-diagram-canvas";

/** Conceptual ER tree aligned with FK relationships in SQLAlchemy models. */
const ER_TREE: ERTreeNode = {
  id: "institution",
  label: "institutions",
  children: [
    {
      id: "users",
      label: "users",
      children: [
        { id: "students", label: "students" },
        { id: "faculty", label: "faculty" },
        { id: "parents", label: "parents" },
      ],
    },
    {
      id: "departments",
      label: "departments",
      children: [
        { id: "programs", label: "programs" },
        { id: "courses", label: "courses" },
      ],
    },
    {
      id: "academic_years",
      label: "academic_years",
      children: [{ id: "semesters", label: "semesters" }],
    },
    {
      id: "academic-core",
      label: "Academic records",
      children: [
        {
          id: "enrollments",
          label: "enrollments",
          children: [
            { id: "assessment_marks", label: "assessment_marks" },
            { id: "attendances", label: "attendances" },
            { id: "course_results", label: "course_results" },
          ],
        },
        { id: "assessments", label: "assessments" },
        { id: "semester_results", label: "semester_results" },
        { id: "prediction_results", label: "prediction_results" },
        { id: "student_goals", label: "student_goals" },
      ],
    },
    {
      id: "links",
      label: "Assignment links",
      children: [
        { id: "faculty_courses", label: "faculty_courses" },
        { id: "faculty_students", label: "faculty_students" },
        { id: "parent_students", label: "parent_students" },
      ],
    },
  ],
};

export function ERDiagram() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Entity relationship view</CardTitle>
        <p className="text-sm text-muted-foreground">
          Hierarchical view of tables and how academic data hangs off the
          institution tenant. Junction tables (parent_students, faculty_students,
          faculty_courses) model many-to-many links.
        </p>
      </CardHeader>
      <CardContent>
        <ERDiagramCanvas tree={ER_TREE} />
        <p className="mt-3 text-xs text-muted-foreground">
          Read-only diagram for presentation. Not a live database browser. Junction
          tables link faculty, parents, and students to courses.
        </p>
      </CardContent>
    </Card>
  );
}
