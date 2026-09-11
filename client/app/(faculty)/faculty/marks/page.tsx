"use client";

import { MarksEntryPage } from "@/components/academic/marks-entry-page";

export default function FacultyMarksPage() {
  return (
    <MarksEntryPage
      title="Marks Entry"
      description="Enter assessment marks for your assigned students and courses."
      showDepartmentFilter={false}
      triggerPredictionsOnSave
    />
  );
}
