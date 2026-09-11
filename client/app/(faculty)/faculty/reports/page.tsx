"use client";

import { Suspense } from "react";
import { LoadingState } from "@/components/analytics/loading-state";
import { FacultyReportsContent } from "./reports-content";

export default function FacultyReportsPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <FacultyReportsContent />
    </Suspense>
  );
}
