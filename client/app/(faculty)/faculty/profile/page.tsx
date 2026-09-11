import { AccountProfileView } from "@/components/layout/account-profile-view";
import { ROUTES } from "@/lib/constants";

export default function FacultyProfilePage() {
  return (
    <AccountProfileView
      breadcrumbs={[
        { label: "Faculty", href: ROUTES.faculty.dashboard },
        { label: "Profile" },
      ]}
    />
  );
}
