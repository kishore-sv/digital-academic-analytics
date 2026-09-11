"use client";

import { StudentTable } from "@/components/analytics/student-table";
import { DataListPage } from "@/components/layout/data-list-page";
import { ROUTES } from "@/lib/constants";
import { useStudents } from "@/hooks/use-students";

export default function FacultyStudentsPage() {
  const { data, isLoading, error } = useStudents();
  const students = data?.data ?? [];

  return (
    <DataListPage
      title="Assigned Students"
      description="Students assigned to you for monitoring."
      isLoading={isLoading}
      error={error}
      isEmpty={students.length === 0}
      emptyTitle="No assigned students"
    >
      <StudentTable
        students={students}
        detailHref={(id) => `${ROUTES.faculty.students}/${id}`}
      />
    </DataListPage>
  );
}
