import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminAnalyticsPage() {
  return (
    <PlaceholderPage
      title="Analytics"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Analytics" },
      ]}
      description="Institutional, department, and subject analytics"
    />
  );
}
