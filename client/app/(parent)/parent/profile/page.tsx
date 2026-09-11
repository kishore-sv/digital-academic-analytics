import { AccountProfileView } from "@/components/layout/account-profile-view";
import { ROUTES } from "@/lib/constants";

export default function ParentProfilePage() {
  return (
    <AccountProfileView
      breadcrumbs={[
        { label: "Parent", href: ROUTES.parent.dashboard },
        { label: "Profile" },
      ]}
    />
  );
}
