"use client";

import { useMemo, useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import {
  MarksEntryFiltersBar,
  MarksEntryAppliedSummary,
  type MarksEntryFilters,
} from "@/components/academic/marks-entry-filters";
import { MarksEntryTable } from "@/components/academic/marks-entry-table";
import {
  useBulkMarksGridMutation,
  useMarksGrid,
  useRegeneratePredictions,
} from "@/hooks/use-academic-entry";
import { showErrorToast } from "@/lib/toast";

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
  const [filtersApplied, setFiltersApplied] = useState(false);

  const gridFilters = useMemo(
    () => ({
      course_id: appliedFilters.course_id,
      semester_id: appliedFilters.semester_id,
      department_id: appliedFilters.department_id,
      program_id: appliedFilters.program_id,
      batch_id: appliedFilters.batch_id,
      class_group_id: appliedFilters.class_group_id,
      section_id: appliedFilters.section_id,
      year_number: appliedFilters.year_number,
      assessment_id: appliedFilters.assessment_id,
      search: appliedFilters.search,
    }),
    [appliedFilters],
  );

  const { data: grid, isLoading, isError, error, refetch } = useMarksGrid(
    gridFilters,
    Boolean(appliedFilters.course_id) && filtersApplied,
  );

  const bulkSave = useBulkMarksGridMutation();
  const regenerate = useRegeneratePredictions();

  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />
      <MarksEntryFiltersBar
        value={draftFilters}
        onChange={setDraftFilters}
        onApply={() => {
          if (!draftFilters.course_id) {
            showErrorToast({
              description: "Select a semester and course, then apply filters.",
            });
            return;
          }
          if (!draftFilters.semester_id) {
            showErrorToast({
              description: "Select a semester for this marks entry context.",
            });
            return;
          }
          setAppliedFilters({ ...draftFilters });
          setFiltersApplied(true);
        }}
        onReset={() => {
          setDraftFilters({});
          setAppliedFilters({});
          setFiltersApplied(false);
        }}
        showDepartment={showDepartmentFilter}
      />
      {filtersApplied && appliedFilters.course_id && (
        <MarksEntryAppliedSummary
          filters={appliedFilters}
          showDepartment={showDepartmentFilter}
        />
      )}
      {isError && (
        <p className="text-sm text-destructive">
          {error instanceof Error ? error.message : "Failed to load marks roster."}
        </p>
      )}
      <MarksEntryTable
        grid={grid}
        isLoading={isLoading}
        isSaving={bulkSave.isPending}
        isRegenerating={regenerate.isPending}
        hasAppliedFilters={filtersApplied && Boolean(appliedFilters.course_id)}
        emptyContext={
          <MarksEntryAppliedSummary
            filters={appliedFilters}
            showDepartment={showDepartmentFilter}
            inline
          />
        }
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
