import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function ParentPredictionsPage() {
  return (
    <PlaceholderPage
      title="Predictions"
      breadcrumbs={[
        { label: "Parent", href: "/parent/dashboard" },
        { label: "Predictions" },
      ]}
      description="Performance predictions for your child"
    />
  );
}
