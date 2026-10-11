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
import { Input } from "@/components/ui/input";
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
import { useAllCourses, usePrograms } from "@/hooks/use-academic";
import {
  useCreateProgramCourse,
  useProgramCourses,
} from "@/hooks/use-academic-structure";

export default function AdminCurriculumPage() {
  const { data: programData } = usePrograms();
  const programs = programData?.data ?? [];
  const [programId, setProgramId] = useState("");
  const pid = programId || programs[0]?.id || "";
  const { data: mappingData, isLoading, error } = useProgramCourses(pid);
  const mappings = mappingData?.data ?? [];
  const { data: courses = [] } = useAllCourses();
  const createMapping = useCreateProgramCourse();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ course_id: "", semester_number: "1" });

  const courseName = (id: string) =>
    courses.find((c) => c.id === id)?.code ?? id.slice(0, 8);

  const handleCreate = async () => {
    if (!pid || !form.course_id) return;
    await createMapping.mutateAsync({
      program_id: pid,
      course_id: form.course_id,
      semester_number: Number(form.semester_number),
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Curriculum"
      description="Map courses to program semesters."
      isLoading={isLoading}
      error={error}
      isEmpty={mappings.length === 0}
      emptyTitle="No curriculum mappings"
    >
      <div className="mb-4 flex flex-wrap justify-between gap-3">
        <Select value={pid} onValueChange={(v) => setProgramId(v ?? "")}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Program" />
          </SelectTrigger>
          <SelectContent>
            {programs.map((p) => (
              <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add mapping</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Program course</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
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
                <Label>Semester number</Label>
                <Input
                  type="number"
                  min={1}
                  max={12}
                  value={form.semester_number}
                  onChange={(e) =>
                    setForm({ ...form, semester_number: e.target.value })
                  }
                />
              </div>
              <Button onClick={handleCreate} disabled={createMapping.isPending}>
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
            <TableHead>Course</TableHead>
            <TableHead>Semester #</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {mappings.map((m, index) => (
            <TableRow key={m.id}>
              <TableSerialCell index={index} />
              <TableCell>{courseName(m.course_id)}</TableCell>
              <TableCell>{m.semester_number}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
