import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminAtRiskPage() {
  return (
    <PlaceholderPage
      title="At-Risk Students"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "At-Risk" },
      ]}
      description="Identify and monitor at-risk students"
    />
  );
}
