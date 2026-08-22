import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentDashboardPage() {
  return (
    <PlaceholderPage
      title="Student Dashboard"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Dashboard" },
      ]}
      description="Your academic overview"
    />
  );
}
