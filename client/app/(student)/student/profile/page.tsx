import { PlaceholderPage } from "@/components/layout/placeholder-page";

export default function StudentProfilePage() {
  return (
    <PlaceholderPage
      title="Profile"
      breadcrumbs={[
        { label: "Student", href: "/student/dashboard" },
        { label: "Profile" },
      ]}
      description="Your academic profile"
    />
  );
}
