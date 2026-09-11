"use client";

import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { PasswordInput } from "@/components/ui/password-input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { StudentTable } from "@/components/analytics/student-table";
import { DataListPage } from "@/components/layout/data-list-page";
import { useDepartments, usePrograms } from "@/hooks/use-academic";
import {
  useCreateStudent,
  useDeleteStudent,
  useStudents,
} from "@/hooks/use-students";

export default function AdminStudentsPage() {
  const { data, isLoading, error } = useStudents();
  const { data: deptData } = useDepartments();
  const { data: programData } = usePrograms();
  const students = data?.data ?? [];
  const departments = deptData?.data ?? [];
  const programs = programData?.data ?? [];
  const departmentItems = departments.map((d) => ({
    value: d.id,
    label: d.name,
  }));
  const programItems = programs.map((p) => ({
    value: p.id,
    label: p.name,
  }));
  const createStudent = useCreateStudent();
  const deleteStudent = useDeleteStudent();
  const [filters, setFilters] = useState({
    department_id: "all",
    branch: "all",
    semester: "all",
  });
  const departmentFilterItems = [
    { value: "all", label: "All Departments" },
    ...departmentItems,
  ];
  const branchFilterItems = useMemo(() => {
    const branches = [...new Set(students.map((s) => s.branch))].sort();
    return [
      { value: "all", label: "All Branches" },
      ...branches.map((branch) => ({ value: branch, label: branch })),
    ];
  }, [students]);
  const semesterFilterItems = useMemo(() => {
    const semesters = [...new Set(students.map((s) => s.semester))].sort(
      (a, b) => a - b,
    );
    return [
      { value: "all", label: "All Semesters" },
      ...semesters.map((semester) => ({
        value: String(semester),
        label: `Semester ${semester}`,
      })),
    ];
  }, [students]);
  const filteredStudents = useMemo(
    () =>
      students.filter((student) => {
        if (
          filters.department_id !== "all" &&
          student.department_id !== filters.department_id
        ) {
          return false;
        }
        if (filters.branch !== "all" && student.branch !== filters.branch) {
          return false;
        }
        if (
          filters.semester !== "all" &&
          student.semester !== Number(filters.semester)
        ) {
          return false;
        }
        return true;
      }),
    [students, filters],
  );
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    name: "",
    roll_number: "",
    password: "",
    department_id: "",
    program_id: "",
    semester: "1",
    branch: "CSE",
  });

  const handleCreate = async () => {
    try {
      await createStudent.mutateAsync({
        name: form.name,
        roll_number: form.roll_number,
        password: form.password,
        department_id: form.department_id,
        program_id: form.program_id || undefined,
        semester: parseInt(form.semester, 10),
        branch: form.branch,
      });
      setOpen(false);
      setForm({
        name: "",
        roll_number: "",
        password: "",
        department_id: "",
        program_id: "",
        semester: "1",
        branch: "CSE",
      });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Students"
      description="All students in your institution."
      isLoading={isLoading}
      error={error}
      isEmpty={students.length === 0}
      emptyTitle="No students found"
    >
      <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div className="flex flex-wrap gap-3">
          <Select
            items={departmentFilterItems}
            value={filters.department_id}
            onValueChange={(value) => {
              if (!value) return;
              setFilters((current) => ({ ...current, department_id: value }));
            }}
          >
            <SelectTrigger className="w-auto min-w-72 max-w-80">
              <SelectValue placeholder="Department" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Departments</SelectItem>
              {departments.map((d) => (
                <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select
            items={branchFilterItems}
            value={filters.branch}
            onValueChange={(value) => {
              if (!value) return;
              setFilters((current) => ({ ...current, branch: value }));
            }}
          >
            <SelectTrigger className="w-auto min-w-40">
              <SelectValue placeholder="Branch" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Branches</SelectItem>
              {branchFilterItems
                .filter((item) => item.value !== "all")
                .map((item) => (
                  <SelectItem key={item.value} value={item.value}>
                    {item.label}
                  </SelectItem>
                ))}
            </SelectContent>
          </Select>
          <Select
            items={semesterFilterItems}
            value={filters.semester}
            onValueChange={(value) => {
              if (!value) return;
              setFilters((current) => ({ ...current, semester: value }));
            }}
          >
            <SelectTrigger className="w-auto min-w-40">
              <SelectValue placeholder="Semester" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Semesters</SelectItem>
              {semesterFilterItems
                .filter((item) => item.value !== "all")
                .map((item) => (
                  <SelectItem key={item.value} value={item.value}>
                    {item.label}
                  </SelectItem>
                ))}
            </SelectContent>
          </Select>
        </div>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Student</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Student</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Name</Label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Roll Number</Label>
                <Input
                  value={form.roll_number}
                  onChange={(e) =>
                    setForm({ ...form, roll_number: e.target.value })
                  }
                />
              </div>
              <div className="space-y-1">
                <Label>Password</Label>
                <PasswordInput
                  autoComplete="new-password"
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                />
              </div>
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
                <Label>Program (optional)</Label>
                <Select
                  items={programItems}
                  value={form.program_id}
                  onValueChange={(v) =>
                    setForm({ ...form, program_id: v ?? "" })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select program" />
                  </SelectTrigger>
                  <SelectContent>
                    {programs.map((p) => (
                      <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1">
                  <Label>Semester</Label>
                  <Input
                    type="number"
                    value={form.semester}
                    onChange={(e) =>
                      setForm({ ...form, semester: e.target.value })
                    }
                  />
                </div>
                <div className="space-y-1">
                  <Label>Branch</Label>
                  <Input
                    value={form.branch}
                    onChange={(e) => setForm({ ...form, branch: e.target.value })}
                  />
                </div>
              </div>
              <Button onClick={handleCreate} disabled={createStudent.isPending}>
                Create
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      {filteredStudents.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No students match the selected filters.
        </p>
      ) : (
        <StudentTable
          students={filteredStudents}
          onDelete={(id) => deleteStudent.mutate(id)}
          deletePending={deleteStudent.isPending}
        />
      )}
    </DataListPage>
  );
}
