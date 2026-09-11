"use client";

import { Suspense } from "react";
import { LoadingState } from "@/components/analytics/loading-state";
import { AdminReportsContent } from "./reports-content";

export default function AdminReportsPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <AdminReportsContent />
    </Suspense>
  );
}
