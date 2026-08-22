import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentGoalsPage() {
  return (
    <PlaceholderPage
      title="Goals"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Goals" },
      ]}
      description="Set and track academic goals"
    />
  );
}
