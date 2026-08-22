import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function ParentDashboardPage() {
  return (
    <PlaceholderPage
      title="Parent Dashboard"
      breadcrumbs={[
        { label: "Parent", href: "/parent/dashboard" },
        { label: "Dashboard" },
      ]}
      description="Overview of your child's academic progress"
    />
  );
}
