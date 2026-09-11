"use client";

import { AttendanceEntryPage } from "@/components/academic/attendance-entry-page";

export default function FacultyAttendancePage() {
  return (
    <AttendanceEntryPage
      title="Attendance Entry"
      description="Update attendance percentages for your assigned students."
      showDepartmentFilter={false}
    />
  );
}
