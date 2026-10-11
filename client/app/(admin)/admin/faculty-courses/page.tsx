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
import { useAllCourses, useFaculty } from "@/hooks/use-academic";
import {
  useAcademicYears,
  useCreateFacultyCourse,
  useFacultyCourses,
  useSections,
  useSemesters,
} from "@/hooks/use-academic-structure";

export default function AdminFacultyCoursesPage() {
  const { data, isLoading, error } = useFacultyCourses(1, 100);
  const rows = data?.data ?? [];
  const { data: facultyData } = useFaculty();
  const faculty = facultyData?.data ?? [];
  const { data: courses = [] } = useAllCourses();
  const { data: years } = useAcademicYears();
  const yearId = years?.find((y) => y.is_current)?.id ?? years?.[0]?.id;
  const { data: semesters } = useSemesters(yearId);
  const { data: sectionData } = useSections();
  const sections = sectionData?.data ?? [];
  const createFc = useCreateFacultyCourse();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    faculty_id: "",
    course_id: "",
    semester_id: "",
    section_id: "",
  });

  const facultyName = (id: string) =>
    faculty.find((f) => f.id === id)?.name ?? id.slice(0, 8);
  const courseName = (id: string) =>
    courses.find((c) => c.id === id)?.code ?? id.slice(0, 8);

  const handleCreate = async () => {
    if (!form.faculty_id || !form.course_id || !form.semester_id) return;
    await createFc.mutateAsync({
      faculty_id: form.faculty_id,
      course_id: form.course_id,
      semester_id: form.semester_id,
      section_id: form.section_id || null,
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Faculty Courses"
      description="Teaching assignments by course and semester."
      isLoading={isLoading}
      error={error}
      isEmpty={rows.length === 0}
      emptyTitle="No assignments"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Assign faculty</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Faculty course assignment</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Faculty</Label>
                <Select
                  value={form.faculty_id}
                  onValueChange={(v) => setForm({ ...form, faculty_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Faculty" />
                  </SelectTrigger>
                  <SelectContent>
                    {faculty.map((f) => (
                      <SelectItem key={f.id} value={f.id}>{f.name}</SelectItem>
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
              <div className="space-y-1">
                <Label>Section (optional)</Label>
                <Select
                  value={form.section_id}
                  onValueChange={(v) => setForm({ ...form, section_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Section" />
                  </SelectTrigger>
                  <SelectContent>
                    {sections.map((s) => (
                      <SelectItem key={s.id} value={s.id}>
                        {s.code} — {s.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <Button onClick={handleCreate} disabled={createFc.isPending}>
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
            <TableHead>Faculty</TableHead>
            <TableHead>Course</TableHead>
            <TableHead>Section</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((r, index) => (
            <TableRow key={r.id}>
              <TableSerialCell index={index} />
              <TableCell>{facultyName(r.faculty_id)}</TableCell>
              <TableCell>{courseName(r.course_id)}</TableCell>
              <TableCell>{r.section_id?.slice(0, 8) ?? "All"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
