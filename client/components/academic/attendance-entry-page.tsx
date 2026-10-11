"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import {
  MarksEntryAppliedSummary,
  MarksEntryFiltersBar,
  type MarksEntryFilters,
} from "@/components/academic/marks-entry-filters";
import { AttendanceEntryTable } from "@/components/academic/attendance-entry-table";
import {
  useAttendanceRoster,
  useBulkAttendanceMutation,
} from "@/hooks/use-academic-entry";

interface AttendanceEntryPageProps {
  title: string;
  description: string;
  showDepartmentFilter?: boolean;
}

export function AttendanceEntryPage({
  title,
  description,
  showDepartmentFilter = true,
}: AttendanceEntryPageProps) {
  const [draftFilters, setDraftFilters] = useState<MarksEntryFilters>({});
  const [appliedFilters, setAppliedFilters] = useState<MarksEntryFilters>({});
  const [hasApplied, setHasApplied] = useState(false);

  const { data: roster, isLoading, isFetching, refetch } = useAttendanceRoster(
    {
      course_id: appliedFilters.course_id,
      academic_year_id: appliedFilters.academic_year_id,
      semester_id: appliedFilters.semester_id,
      department_id: appliedFilters.department_id,
      program_id: appliedFilters.program_id,
      batch_id: appliedFilters.batch_id,
      class_group_id: appliedFilters.class_group_id,
      section_id: appliedFilters.section_id,
      year_number: appliedFilters.year_number,
      search: appliedFilters.search,
      date_from: appliedFilters.date_from,
      date_to: appliedFilters.date_to,
      status: appliedFilters.attendance_status,
    },
    hasApplied,
  );

  const bulkSave = useBulkAttendanceMutation();
  const showRange = Boolean(appliedFilters.date_from || appliedFilters.date_to);

  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />
      <MarksEntryFiltersBar
        mode="attendance"
        value={draftFilters}
        onChange={setDraftFilters}
        onApply={() => {
          setAppliedFilters({ ...draftFilters });
          setHasApplied(true);
        }}
        onReset={() => {
          setDraftFilters({});
          setAppliedFilters({});
          setHasApplied(false);
        }}
        showDepartment={showDepartmentFilter}
      />
      {hasApplied && (
        <MarksEntryAppliedSummary
          filters={appliedFilters}
          showDepartment={showDepartmentFilter}
        />
      )}
      <AttendanceEntryTable
        roster={roster}
        isLoading={hasApplied && (isLoading || isFetching)}
        hasApplied={hasApplied}
        showRange={showRange}
        canEdit={Boolean(appliedFilters.course_id)}
        isSaving={bulkSave.isPending}
        onSave={async (entries) => {
          await bulkSave.mutateAsync(entries);
          refetch();
        }}
      />
    </div>
  );
}
