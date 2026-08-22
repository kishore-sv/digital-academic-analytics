import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyAtRiskPage() {
  return (
    <PlaceholderPage
      title="At-Risk Students"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "At-Risk" },
      ]}
      description="At-risk students in your assigned group"
    />
  );
}
