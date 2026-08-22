import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminStudentsPage() {
  return (
    <PlaceholderPage
      title="Students"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Students" },
      ]}
      description="Manage student accounts and academic information"
    />
  );
}
