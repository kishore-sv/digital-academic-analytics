import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentPerformancePage() {
  return (
    <PlaceholderPage
      title="Performance"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Performance" },
      ]}
      description="View your academic performance"
    />
  );
}
