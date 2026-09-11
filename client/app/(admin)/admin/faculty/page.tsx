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
  useCreateFaculty,
  useDeleteFaculty,
} from "@/hooks/use-academic-mutations";
import { useDepartments, useFaculty } from "@/hooks/use-academic";

export default function AdminFacultyPage() {
  const { data, isLoading, error } = useFaculty();
  const { data: deptData } = useDepartments();
  const faculty = data?.data ?? [];
  const departments = deptData?.data ?? [];
  const departmentItems = departments.map((d) => ({
    value: d.id,
    label: d.name,
  }));
  const createFaculty = useCreateFaculty();
  const deleteFaculty = useDeleteFaculty();
  const [departmentFilter, setDepartmentFilter] = useState("all");
  const departmentFilterItems = [
    { value: "all", label: "All Departments" },
    ...departmentItems,
  ];
  const filteredFaculty = useMemo(
    () =>
      faculty.filter((member) =>
        departmentFilter === "all"
          ? true
          : member.department_id === departmentFilter,
      ),
    [faculty, departmentFilter],
  );
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    department_id: "",
  });

  const handleCreate = async () => {
    try {
      await createFaculty.mutateAsync(form);
      setOpen(false);
      setForm({ name: "", email: "", password: "", department_id: "" });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Faculty"
      description="Faculty members in your institution."
      isLoading={isLoading}
      error={error}
      isEmpty={faculty.length === 0}
      emptyTitle="No faculty found"
    >
      <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <Select
          items={departmentFilterItems}
          value={departmentFilter}
          onValueChange={(value) => {
            if (!value) return;
            setDepartmentFilter(value);
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
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Faculty</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Faculty Member</DialogTitle>
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
                <Label>Email</Label>
                <Input
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Password</Label>
                <PasswordInput
                  autoComplete="new-password"
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
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
              <Button onClick={handleCreate} disabled={createFaculty.isPending}>
                Create
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      {filteredFaculty.length === 0 ? (
        <p className="text-sm text-muted-foreground">
          No faculty match the selected filters.
        </p>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableSerialHead />
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Department</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredFaculty.map((f, index) => (
              <TableRow key={f.id}>
                <TableSerialCell index={index} />
                <TableCell>{f.name}</TableCell>
                <TableCell>{f.email ?? "—"}</TableCell>
                <TableCell>
                  {departments.find((d) => d.id === f.department_id)?.name ??
                    f.department_id}
                </TableCell>
                <TableCell className="text-right">
                  <DeleteConfirmButton
                    itemName={f.name}
                    onConfirm={() => deleteFaculty.mutate(f.id)}
                    pending={deleteFaculty.isPending}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </DataListPage>
  );
}
