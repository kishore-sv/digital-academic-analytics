import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyDashboardPage() {
  return (
    <PlaceholderPage
      title="Faculty Dashboard"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "Dashboard" },
      ]}
      description="Overview of assigned students"
    />
  );
}
