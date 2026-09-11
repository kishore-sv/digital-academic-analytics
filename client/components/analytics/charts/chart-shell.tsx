"use client";

import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";

interface ChartShellProps {
  title?: string;
  isLoading?: boolean;
  error?: Error | null;
  isEmpty?: boolean;
  emptyTitle?: string;
  children: React.ReactNode;
}

export function ChartShell({
  title,
  isLoading,
  error,
  isEmpty,
  emptyTitle = "No data available",
  children,
}: ChartShellProps) {
  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState title="Error" description={error.message} />;
  if (isEmpty) return <EmptyState title={emptyTitle} />;
  return (
    <div className="space-y-2">
      {title && <p className="text-sm font-medium text-muted-foreground">{title}</p>}
      {children}
    </div>
  );
}
