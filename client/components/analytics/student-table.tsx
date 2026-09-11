import Link from "next/link";
import { DeleteConfirmButton } from "@/components/layout/delete-confirm-button";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Student } from "@/hooks/use-students";

interface StudentTableProps {
  students: Student[];
  detailHref?: (studentId: string) => string;
  onDelete?: (studentId: string) => void;
  deletePending?: boolean;
  serialStart?: number;
}

export function StudentTable({
  students,
  detailHref,
  onDelete,
  deletePending,
  serialStart = 1,
}: StudentTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableSerialHead />
          <TableHead>Roll Number</TableHead>
          <TableHead>Name</TableHead>
          <TableHead>Branch</TableHead>
          <TableHead>Semester</TableHead>
          {(detailHref || onDelete) && (
            <TableHead className="text-right">Actions</TableHead>
          )}
        </TableRow>
      </TableHeader>
      <TableBody>
        {students.map((student, index) => (
          <TableRow key={student.id}>
            <TableSerialCell index={index} start={serialStart} />
            <TableCell className="font-mono text-sm">{student.roll_number}</TableCell>
            <TableCell>{student.name}</TableCell>
            <TableCell>{student.branch}</TableCell>
            <TableCell>{student.semester}</TableCell>
            {(detailHref || onDelete) && (
              <TableCell className="space-x-2 text-right">
                {detailHref && (
                  <Link
                    href={detailHref(student.id)}
                    className="text-sm text-primary underline-offset-4 hover:underline"
                  >
                    View
                  </Link>
                )}
                {onDelete && (
                  <DeleteConfirmButton
                    itemName={student.name}
                    onConfirm={() => onDelete(student.id)}
                    pending={deletePending}
                  />
                )}
              </TableCell>
            )}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
