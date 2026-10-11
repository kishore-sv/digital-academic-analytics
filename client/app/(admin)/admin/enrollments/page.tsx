"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { DataListPage } from "@/components/layout/data-list-page";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import { useAllCourses } from "@/hooks/use-academic";
import {
  useAcademicYears,
  useCreateEnrollment,
  useEnrollments,
  useSemesters,
} from "@/hooks/use-academic-structure";
import { useStudents } from "@/hooks/use-students";

export default function AdminEnrollmentsPage() {
  const { data, isLoading, error } = useEnrollments(1, 100);
  const enrollments = data?.data ?? [];
  const { data: studentData } = useStudents(1, 100);
  const students = studentData?.data ?? [];
  const { data: courses = [] } = useAllCourses();
  const { data: years } = useAcademicYears();
  const yearId = years?.find((y) => y.is_current)?.id ?? years?.[0]?.id;
  const { data: semesters } = useSemesters(yearId);
  const createEnrollment = useCreateEnrollment();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    student_id: "",
    course_id: "",
    semester_id: "",
  });

  const studentName = (id: string) =>
    students.find((s) => s.id === id)?.roll_number ?? id.slice(0, 8);
  const courseName = (id: string) =>
    courses.find((c) => c.id === id)?.code ?? id.slice(0, 8);

  const handleCreate = async () => {
    if (!form.student_id || !form.course_id || !form.semester_id) return;
    await createEnrollment.mutateAsync({
      student_id: form.student_id,
      course_id: form.course_id,
      semester_id: form.semester_id,
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Enrollments"
      description="Student course registrations by semester."
      isLoading={isLoading}
      error={error}
      isEmpty={enrollments.length === 0}
      emptyTitle="No enrollments"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add enrollment</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>New enrollment</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Student</Label>
                <Select
                  value={form.student_id}
                  onValueChange={(v) => setForm({ ...form, student_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Student" />
                  </SelectTrigger>
                  <SelectContent>
                    {students.map((s) => (
                      <SelectItem key={s.id} value={s.id}>
                        {s.roll_number} — {s.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <Label>Course</Label>
                <Select
                  value={form.course_id}
                  onValueChange={(v) => setForm({ ...form, course_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Course" />
                  </SelectTrigger>
                  <SelectContent>
                    {courses.map((c) => (
                      <SelectItem key={c.id} value={c.id}>
                        {c.code} — {c.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <Label>Semester</Label>
                <Select
                  value={form.semester_id}
                  onValueChange={(v) => setForm({ ...form, semester_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Semester" />
                  </SelectTrigger>
                  <SelectContent>
                    {semesters?.map((s) => (
                      <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleCreate} disabled={createEnrollment.isPending}>
                Create
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableSerialHead />
            <TableHead>Student</TableHead>
            <TableHead>Course</TableHead>
            <TableHead>Attendance %</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {enrollments.map((e, index) => (
            <TableRow key={e.id}>
              <TableSerialCell index={index} />
              <TableCell>{studentName(e.student_id)}</TableCell>
              <TableCell>{courseName(e.course_id)}</TableCell>
              <TableCell>{e.attendance_percentage ?? "—"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
