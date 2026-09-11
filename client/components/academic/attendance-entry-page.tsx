"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import {
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

  const { data: roster, isLoading, refetch } = useAttendanceRoster(
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

  const bulkSave = useBulkAttendanceMutation();

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
      <AttendanceEntryTable
        roster={roster}
        isLoading={isLoading}
        isSaving={bulkSave.isPending}
        onSave={async (entries) => {
          await bulkSave.mutateAsync(entries);
          refetch();
        }}
      />
    </div>
  );
}
