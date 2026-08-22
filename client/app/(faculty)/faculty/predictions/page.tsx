import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function FacultyPredictionsPage() {
  return (
    <PlaceholderPage
      title="Predictions"
      breadcrumbs={[
        { label: "Faculty", href: "/faculty/dashboard" },
        { label: "Predictions" },
      ]}
      description="Performance predictions for assigned students"
    />
  );
}
