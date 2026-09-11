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
  useCreateProgram,
  useDeleteProgram,
} from "@/hooks/use-academic-mutations";
import { useDepartments, usePrograms } from "@/hooks/use-academic";

export default function AdminProgramsPage() {
  const { data, isLoading, error } = usePrograms();
  const { data: deptData } = useDepartments();
  const programs = data?.data ?? [];
  const departments = deptData?.data ?? [];
  const departmentItems = departments.map((d) => ({
    value: d.id,
    label: d.name,
  }));
  const createProgram = useCreateProgram();
  const deleteProgram = useDeleteProgram();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    department_id: "",
    name: "",
    code: "",
    duration_semesters: "8",
  });

  const handleCreate = async () => {
    try {
      await createProgram.mutateAsync({
        department_id: form.department_id,
        name: form.name,
        code: form.code,
        duration_semesters: parseInt(form.duration_semesters, 10),
      });
      setOpen(false);
      setForm({ department_id: "", name: "", code: "", duration_semesters: "8" });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Programs"
      description="Academic programs offered per department."
      isLoading={isLoading}
      error={error}
      isEmpty={programs.length === 0}
      emptyTitle="No programs found"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Program</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Program</DialogTitle>
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
                <Label>Duration (semesters)</Label>
                <Input
                  type="number"
                  value={form.duration_semesters}
                  onChange={(e) =>
                    setForm({ ...form, duration_semesters: e.target.value })
                  }
                />
              </div>
              <Button onClick={handleCreate} disabled={createProgram.isPending}>
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
            <TableHead>Duration</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {programs.map((p, index) => (
            <TableRow key={p.id}>
              <TableSerialCell index={index} />
              <TableCell>{p.code}</TableCell>
              <TableCell>{p.name}</TableCell>
              <TableCell>{p.duration_semesters} sem</TableCell>
              <TableCell className="text-right">
                <DeleteConfirmButton
                  itemName={p.name}
                  onConfirm={() => deleteProgram.mutate(p.id)}
                  pending={deleteProgram.isPending}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
