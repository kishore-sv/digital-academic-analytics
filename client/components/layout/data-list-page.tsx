"use client";

import { EmptyState } from "@/components/analytics/empty-state";
import { ErrorState } from "@/components/analytics/error-state";
import { LoadingState } from "@/components/analytics/loading-state";
import { PageHeader } from "@/components/layout/page-header";

interface DataListPageProps {
  title: string;
  description?: string;
  isLoading: boolean;
  error: unknown;
  isEmpty: boolean;
  emptyTitle: string;
  emptyDescription?: string;
  children: React.ReactNode;
}

export function DataListPage({
  title,
  description,
  isLoading,
  error,
  isEmpty,
  emptyTitle,
  emptyDescription,
  children,
}: DataListPageProps) {
  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />
      {isLoading && <LoadingState />}
      {error ? (
        <ErrorState description="Unable to load data from the API." />
      ) : null}
      {!isLoading && !error && isEmpty && (
        <EmptyState title={emptyTitle} description={emptyDescription} />
      )}
      {!isLoading && !error && !isEmpty && children}
    </div>
  );
}
