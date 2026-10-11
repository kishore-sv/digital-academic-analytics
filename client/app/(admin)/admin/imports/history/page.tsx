"use client";

import Link from "next/link";
import { DataListPage } from "@/components/layout/data-list-page";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useImportJobs } from "@/hooks/use-master-import";
import { ROUTES } from "@/lib/constants";

export default function ImportHistoryPage() {
  const { data, isLoading, error } = useImportJobs(1, 50);
  const jobs = data?.data ?? [];

  return (
    <DataListPage
      title="Import history"
      description="Past master data import attempts for your institution."
      isLoading={isLoading}
      error={error}
      isEmpty={jobs.length === 0}
      emptyTitle="No imports yet"
    >
      <div className="mb-4">
        <Button variant="outline" render={<Link href={ROUTES.admin.imports} />}>
          Back to Import Center
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableSerialHead />
            <TableHead>Type</TableHead>
            <TableHead>File</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Rows</TableHead>
            <TableHead>Created</TableHead>
            <TableHead>Success</TableHead>
            <TableHead>Errors</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {jobs.map((job, index) => (
            <TableRow key={job.id}>
              <TableSerialCell index={index} />
              <TableCell className="font-mono text-xs">
                {job.import_type}
              </TableCell>
              <TableCell>{job.filename}</TableCell>
              <TableCell>{job.status}</TableCell>
              <TableCell>{job.total_rows}</TableCell>
              <TableCell>
                {new Date(job.created_at).toLocaleString()}
              </TableCell>
              <TableCell>{job.created_rows}</TableCell>
              <TableCell>{job.failed_rows + job.invalid_rows}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
