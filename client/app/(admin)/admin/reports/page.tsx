import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminReportsPage() {
  return (
    <PlaceholderPage
      title="Reports"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Reports" },
      ]}
      description="Academic reports with alerts and trends"
    />
  );
}
