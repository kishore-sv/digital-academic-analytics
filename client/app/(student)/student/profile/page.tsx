import { AccountProfileView } from "@/components/layout/account-profile-view";
import { ROUTES } from "@/lib/constants";

export default function StudentProfilePage() {
  return (
    <AccountProfileView
      breadcrumbs={[
        { label: "Student", href: ROUTES.student.dashboard },
        { label: "Profile" },
      ]}
    />
  );
}
