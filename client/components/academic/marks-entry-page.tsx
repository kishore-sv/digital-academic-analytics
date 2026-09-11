"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import {
  MarksEntryFiltersBar,
  type MarksEntryFilters,
} from "@/components/academic/marks-entry-filters";
import { MarksEntryTable } from "@/components/academic/marks-entry-table";
import {
  useBulkMarksGridMutation,
  useMarksGrid,
  useRegeneratePredictions,
} from "@/hooks/use-academic-entry";

interface MarksEntryPageProps {
  title: string;
  description: string;
  showDepartmentFilter?: boolean;
  triggerPredictionsOnSave?: boolean;
}

export function MarksEntryPage({
  title,
  description,
  showDepartmentFilter = true,
  triggerPredictionsOnSave = false,
}: MarksEntryPageProps) {
  const [draftFilters, setDraftFilters] = useState<MarksEntryFilters>({});
  const [appliedFilters, setAppliedFilters] = useState<MarksEntryFilters>({});

  const { data: grid, isLoading, refetch } = useMarksGrid(
    {
      course_id: appliedFilters.course_id,
      semester_id: appliedFilters.semester_id,
      department_id: appliedFilters.department_id,
      program_id: appliedFilters.program_id,
      section: appliedFilters.section,
      search: appliedFilters.search,
    },
    Boolean(appliedFilters.course_id),
  );

  const bulkSave = useBulkMarksGridMutation();
  const regenerate = useRegeneratePredictions();

  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />
      <MarksEntryFiltersBar
        value={draftFilters}
        onChange={setDraftFilters}
        onApply={() => setAppliedFilters({ ...draftFilters })}
        onReset={() => {
          setDraftFilters({});
          setAppliedFilters({});
        }}
        showDepartment={showDepartmentFilter}
      />
      <MarksEntryTable
        grid={grid}
        isLoading={isLoading}
        isSaving={bulkSave.isPending}
        isRegenerating={regenerate.isPending}
        onSave={async (entries) => {
          await bulkSave.mutateAsync({
            entries,
            trigger_predictions: triggerPredictionsOnSave,
          });
          refetch();
        }}
        onRegenerate={() => regenerate.mutate()}
      />
    </div>
  );
}
