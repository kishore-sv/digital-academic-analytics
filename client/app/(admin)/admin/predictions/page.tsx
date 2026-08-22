import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function AdminPredictionsPage() {
  return (
    <PlaceholderPage
      title="Predictions"
      breadcrumbs={[
        { label: "Admin", href: "/admin/dashboard" },
        { label: "Predictions" },
      ]}
      description="ML-powered performance predictions"
    />
  );
}
