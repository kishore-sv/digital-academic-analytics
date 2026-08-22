import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyReportsPage() {
  return (
    <PlaceholderPage
      title="Reports"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "Reports" },
      ]}
      description="Reports for assigned students"
    />
  );
}
