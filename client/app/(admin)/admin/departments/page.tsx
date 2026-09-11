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
  useCreateDepartment,
  useDeleteDepartment,
} from "@/hooks/use-academic-mutations";
import { useDepartments } from "@/hooks/use-academic";

export default function AdminDepartmentsPage() {
  const { data, isLoading, error } = useDepartments();
  const departments = data?.data ?? [];
  const createDepartment = useCreateDepartment();
  const deleteDepartment = useDeleteDepartment();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ name: "", code: "", description: "" });

  const handleCreate = async () => {
    try {
      await createDepartment.mutateAsync({
        name: form.name,
        code: form.code,
        description: form.description || undefined,
      });
      setOpen(false);
      setForm({ name: "", code: "", description: "" });
    } catch {
      // Error toast handled by mutation hook.
    }
  };

  return (
    <DataListPage
      title="Departments"
      description="Academic departments in your institution."
      isLoading={isLoading}
      error={error}
      isEmpty={departments.length === 0}
      emptyTitle="No departments found"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Department</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Department</DialogTitle>
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
                <Label>Code</Label>
                <Input
                  value={form.code}
                  onChange={(e) => setForm({ ...form, code: e.target.value })}
                />
              </div>
              <div className="space-y-1">
                <Label>Description</Label>
                <Input
                  value={form.description}
                  onChange={(e) =>
                    setForm({ ...form, description: e.target.value })
                  }
                />
              </div>
              <Button onClick={handleCreate} disabled={createDepartment.isPending}>
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
            <TableHead>Description</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {departments.map((d, index) => (
            <TableRow key={d.id}>
              <TableSerialCell index={index} />
              <TableCell>{d.code}</TableCell>
              <TableCell>{d.name}</TableCell>
              <TableCell>{d.description ?? "—"}</TableCell>
              <TableCell className="text-right">
                <DeleteConfirmButton
                  itemName={d.name}
                  onConfirm={() => deleteDepartment.mutate(d.id)}
                  pending={deleteDepartment.isPending}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
