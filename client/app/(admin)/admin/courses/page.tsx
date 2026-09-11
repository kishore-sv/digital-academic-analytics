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
import { DeleteConfirmButton } from "@/components/layout/delete-confirm-button";
import { DataListPage } from "@/components/layout/data-list-page";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import {
  useCreateCourse,
  useDeleteCourse,
} from "@/hooks/use-academic-mutations";
import { useCourses, useDepartments } from "@/hooks/use-academic";

export default function AdminCoursesPage() {
  const { data, isLoading, error } = useCourses();
  const { data: deptData } = useDepartments();
  const courses = data?.data ?? [];
  const departments = deptData?.data ?? [];
  const departmentItems = departments.map((d) => ({
    value: d.id,
    label: d.name,
  }));
  const createCourse = useCreateCourse();
  const deleteCourse = useDeleteCourse();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    department_id: "",
    name: "",
    code: "",
    credits: "3",
    course_type: "THEORY",
  });

  const handleCreate = async () => {
    try {
      await createCourse.mutateAsync({
        department_id: form.department_id,
        name: form.name,
        code: form.code,
        credits: parseInt(form.credits, 10),
        course_type: form.course_type,
      });
      setOpen(false);
      setForm({
        department_id: "",
        name: "",
        code: "",
        credits: "3",
        course_type: "THEORY",
      });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Courses"
      description="Courses offered across departments."
      isLoading={isLoading}
      error={error}
      isEmpty={courses.length === 0}
      emptyTitle="No courses found"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Course</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Course</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Department</Label>
                <Select
                  items={departmentItems}
                  value={form.department_id}
                  onValueChange={(v) =>
                    setForm({ ...form, department_id: v ?? "" })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select department" />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map((d) => (
                      <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <Label>Name</Label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Code</Label>
                <Input
                  value={form.code}
                  onChange={(e) => setForm({ ...form, code: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Credits</Label>
                <Input
                  type="number"
                  value={form.credits}
                  onChange={(e) => setForm({ ...form, credits: e.target.value })}
                />
              </div>
              <Button onClick={handleCreate} disabled={createCourse.isPending}>
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
            <TableHead>Code</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Credits</TableHead>
            <TableHead>Type</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {courses.map((c, index) => (
            <TableRow key={c.id}>
              <TableSerialCell index={index} />
              <TableCell>{c.code}</TableCell>
              <TableCell>{c.name}</TableCell>
              <TableCell>{c.credits}</TableCell>
              <TableCell>{c.course_type}</TableCell>
              <TableCell className="text-right">
                <DeleteConfirmButton
                  itemName={c.name}
                  onConfirm={() => deleteCourse.mutate(c.id)}
                  pending={deleteCourse.isPending}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
