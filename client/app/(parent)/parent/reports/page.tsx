"use client";

import { Button } from "@/components/ui/button";
import { PageHeader } from "@/components/layout/page-header";
import { useMyParentProfile } from "@/hooks/use-academic";
import { useReportDownloads } from "@/hooks/use-reports";

export default function ParentReportsPage() {
  const { data: parent } = useMyParentProfile();
  const childId = parent?.linked_student_ids[0];
  const { downloadStudentReport } = useReportDownloads();

  return (
    <div className="space-y-6">
      <PageHeader title="Reports" description="Download your child's academic report." />
      <Button
        disabled={!childId}
        onClick={() => childId && downloadStudentReport(childId)}
      >
        Download Child Prediction Report
      </Button>
    </div>
  );
}
