import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminDashboardPage() {
  return (
    <PlaceholderPage
      title="Admin Dashboard"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Dashboard" },
      ]}
      description="Institutional analytics overview"
    />
  );
}
