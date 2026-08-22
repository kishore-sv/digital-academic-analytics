import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyStudentsPage() {
  return (
    <PlaceholderPage
      title="Students"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "Students" },
      ]}
      description="View assigned students"
    />
  );
}
