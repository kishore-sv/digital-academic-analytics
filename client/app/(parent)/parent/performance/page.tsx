import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function ParentPerformancePage() {
  return (
    <PlaceholderPage
      title="Performance"
      breadcrumbs={[
        { label: "Parent", href: "/parent/dashboard" },
        { label: "Performance" },
      ]}
      description="Your child's academic performance"
    />
  );
}
