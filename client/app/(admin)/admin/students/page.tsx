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
import {
  StudentPlacementSelectors,
  type StudentPlacementValue,
} from "@/components/academic/cascading-selectors";
import { StudentTable } from "@/components/analytics/student-table";
import { DataListPage } from "@/components/layout/data-list-page";
import { useDepartments } from "@/hooks/use-academic";
import {
  useCreateStudent,
  useDeleteStudent,
  useStudents,
} from "@/hooks/use-students";
import { showErrorToast } from "@/lib/toast";

const emptyPlacement = (): StudentPlacementValue => ({
  department_id: "",
  program_id: "",
  batch_id: "",
  class_group_id: "",
  section_id: "",
  current_semester_id: "",
});

export default function AdminStudentsPage() {
  const { data, isLoading, error } = useStudents(1, 100);
  const { data: deptData } = useDepartments();
  const students = data?.data ?? [];
  const departments = deptData?.data ?? [];
  const createStudent = useCreateStudent();
  const deleteStudent = useDeleteStudent();
  const [filters, setFilters] = useState({
    department_id: "all",
    semester: "all",
    section: "all",
  });
  const departmentFilterItems = [
    { value: "all", label: "All Departments" },
    ...departments.map((d) => ({ value: d.id, label: d.name })),
  ];
  const semesterFilterItems = useMemo(() => {
    const semesters = [
      ...new Set(
        students
          .map((s) => s.semester_number)
          .filter((n): n is number => n != null),
      ),
    ].sort((a, b) => a - b);
    return [
      { value: "all", label: "All Semesters" },
      ...semesters.map((semester) => ({
        value: String(semester),
        label: `Semester ${semester}`,
      })),
    ];
  }, [students]);
  const sectionFilterItems = useMemo(() => {
    const codes = [
      ...new Set(
        students.map((s) => s.section_code).filter((c): c is string => Boolean(c)),
      ),
    ].sort();
    return [
      { value: "all", label: "All Sections" },
      ...codes.map((code) => ({ value: code, label: code })),
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
        if (
          filters.semester !== "all" &&
          student.semester_number !== Number(filters.semester)
        ) {
          return false;
        }
        if (
          filters.section !== "all" &&
          student.section_code !== filters.section
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
    placement: emptyPlacement(),
  });

  const handleCreate = async () => {
    const name = form.name.trim();
    const rollNumber = form.roll_number.trim();
    const p = form.placement;

    if (!name || !rollNumber) {
      showErrorToast({ description: "Name and roll number are required." });
      return;
    }
    if (form.password.length < 6) {
      showErrorToast({ description: "Password must be at least 6 characters." });
      return;
    }
    if (
      !p.department_id ||
      !p.program_id ||
      !p.batch_id ||
      !p.class_group_id ||
      !p.section_id ||
      !p.current_semester_id
    ) {
      showErrorToast({
        description: "Complete academic placement (program through section).",
      });
      return;
    }

    try {
      await createStudent.mutateAsync({
        name,
        roll_number: rollNumber,
        password: form.password,
        department_id: p.department_id,
        program_id: p.program_id,
        batch_id: p.batch_id,
        class_group_id: p.class_group_id,
        section_id: p.section_id,
        current_semester_id: p.current_semester_id,
      });
      setOpen(false);
      setForm({ name: "", roll_number: "", password: "", placement: emptyPlacement() });
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
          <Select
            items={sectionFilterItems}
            value={filters.section}
            onValueChange={(value) => {
              if (!value) return;
              setFilters((current) => ({ ...current, section: value }));
            }}
          >
            <SelectTrigger className="w-auto min-w-36">
              <SelectValue placeholder="Section" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Sections</SelectItem>
              {sectionFilterItems
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
          <DialogContent className="max-w-2xl">
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
                  minLength={6}
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                />
              </div>
              {departments.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  Add departments, programs, batches, and sections before creating students.
                </p>
              ) : (
                <StudentPlacementSelectors
                  value={form.placement}
                  onChange={(placement) => setForm({ ...form, placement })}
                />
              )}
              <Button onClick={handleCreate} disabled={createStudent.isPending}>
                Create
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      {filteredStudents.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          {students.length === 0
            ? "No students yet. Click Add Student to create one."
            : "No students match the selected filters."}
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
