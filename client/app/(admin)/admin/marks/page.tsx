"use client";

import { MarksEntryPage } from "@/components/academic/marks-entry-page";

export default function AdminMarksPage() {
  return (
    <MarksEntryPage
      title="Marks Entry"
      description="Enter and manage assessment marks for all students."
      showDepartmentFilter
      triggerPredictionsOnSave
    />
  );
}
