import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentReportsPage() {
  return (
    <PlaceholderPage
      title="Reports"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Reports" },
      ]}
      description="Your academic reports"
    />
  );
}
