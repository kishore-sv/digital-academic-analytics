import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function ParentReportsPage() {
  return (
    <PlaceholderPage
      title="Reports"
      breadcrumbs={[
        { label: "Parent", href: "/parent/dashboard" },
        { label: "Reports" },
      ]}
      description="Academic reports for your child"
    />
  );
}
