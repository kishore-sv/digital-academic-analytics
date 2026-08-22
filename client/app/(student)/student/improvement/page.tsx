import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentImprovementPage() {
  return (
    <PlaceholderPage
      title="Improvement Areas"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Improvement" },
      ]}
      description="Areas for academic improvement"
    />
  );
}
