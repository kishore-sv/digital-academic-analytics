import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminDepartmentsPage() {
  return (
    <PlaceholderPage
      title="Departments"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Departments" },
      ]}
      description="Manage academic departments"
    />
  );
}
