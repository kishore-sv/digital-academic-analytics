import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyPerformancePage() {
  return (
    <PlaceholderPage
      title="Performance"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "Performance" },
      ]}
      description="Student performance for assigned students"
    />
  );
}
