import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function ParentImprovementPage() {
  return (
    <PlaceholderPage
      title="Improvement Areas"
      breadcrumbs={[
        { label: "Parent", href: "/parent/dashboard" },
        { label: "Improvement" },
      ]}
      description="Areas where your child can improve"
    />
  );
}
