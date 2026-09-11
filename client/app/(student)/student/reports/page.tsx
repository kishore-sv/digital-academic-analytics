"use client";

import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/layout/page-header";
import { useMyStudentProfile } from "@/hooks/use-students";
import { useReportDownloads } from "@/hooks/use-reports";

export default function StudentReportsPage() {
  const { data: student } = useMyStudentProfile();
  const { downloadStudentReport } = useReportDownloads();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Download your academic prediction report."
      />
      <Button
        disabled={!student?.id}
        onClick={() => student?.id && downloadStudentReport(student.id)}
      >
        Download Prediction Report
      </Button>
    </div>
  );
}
