"use client";

import { AttendanceEntryPage } from "@/components/academic/attendance-entry-page";

export default function AdminAttendancePage() {
  return (
    <AttendanceEntryPage
      title="Attendance Management"
      description="View and update institution-wide attendance records."
      showDepartmentFilter
    />
  );
}
