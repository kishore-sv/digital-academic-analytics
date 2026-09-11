import { AccountProfileView } from "@/components/layout/account-profile-view";
import { ROUTES } from "@/lib/constants";

export default function AdminProfilePage() {
  return (
    <AccountProfileView
      breadcrumbs={[
        { label: "Admin", href: ROUTES.admin.dashboard },
        { label: "Profile" },
      ]}
    />
  );
}
