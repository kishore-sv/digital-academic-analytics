"use client";

import { useQuery } from "@tanstack/react-query";
import { LoadingState } from "@/components/analytics/loading-state";
import { PageHeader } from "@/components/layout/page-header";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { apiFetch } from "@/lib/api";
import { getRoleLabel, getUserDisplayName } from "@/lib/auth-routes";

interface InstitutionInfo {
  id: string;
  name: string;
}

interface AccountProfileViewProps {
  breadcrumbs?: { label: string; href?: string }[];
}

export function AccountProfileView({ breadcrumbs }: AccountProfileViewProps) {
  const { user, isLoading } = useAuth();

  const { data: institution, isLoading: institutionLoading } =
    useQuery<InstitutionInfo>({
      queryKey: ["institution", "me"],
      queryFn: () => apiFetch<InstitutionInfo>("/institutions/me"),
      enabled: !!user,
    });

  if (isLoading) {
    return <LoadingState message="Loading profile..." compact />;
  }

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Profile"
        description="Your account and institution details"
        breadcrumbs={breadcrumbs}
      />
      <Card className="max-w-xl">
        <CardHeader>
          <CardTitle>{getUserDisplayName(user)}</CardTitle>
          <CardDescription>{getRoleLabel(user.role)}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 text-sm">
          <div className="flex justify-between gap-4 border-b pb-3">
            <span className="text-muted-foreground">Email</span>
            <span className="text-right font-medium">
              {user.email ?? "Not set"}
            </span>
          </div>
          <div className="flex justify-between gap-4 border-b pb-3">
            <span className="text-muted-foreground">Role</span>
            <span className="text-right font-medium">
              {getRoleLabel(user.role)}
            </span>
          </div>
          <div className="flex justify-between gap-4 border-b pb-3">
            <span className="text-muted-foreground">Institution</span>
            <span className="text-right font-medium">
              {institutionLoading
                ? "Loading..."
                : institution?.name ?? "—"}
            </span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-muted-foreground">User ID</span>
            <span className="max-w-[220px] truncate text-right font-mono text-xs">
              {user.id}
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
