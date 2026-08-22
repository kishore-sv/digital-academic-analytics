import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentPredictionsPage() {
  return (
    <PlaceholderPage
      title="Predictions"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Predictions" },
      ]}
      description="ML-powered performance predictions"
    />
  );
}
