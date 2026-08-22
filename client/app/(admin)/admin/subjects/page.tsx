import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminSubjectsPage() {
  return (
    <PlaceholderPage
      title="Subjects"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Subjects" },
      ]}
      description="Manage subjects and courses"
    />
  );
}
