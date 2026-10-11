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
import { PasswordInput } from "@/components/ui/password-input";
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
import { apiFetch } from "@/lib/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { mergeMutationHandlers } from "@/lib/toast";
import type { PaginatedResponse } from "@/types/api";

interface ParentRow {
  id: string;
  name: string;
  phone: string | null;
  linked_student_ids: string[];
}

export default function AdminParentsPage() {
  const qc = useQueryClient();
  const { data, isLoading, error } = useQuery({
    queryKey: ["parents"],
    queryFn: () => apiFetch<PaginatedResponse<ParentRow>>("/parents?limit=100"),
  });
  const parents = data?.data ?? [];
  const createParent = useMutation({
    mutationFn: (body: {
      name: string;
      email: string;
      password: string;
      phone?: string;
    }) =>
      apiFetch<ParentRow>("/parents", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    ...mergeMutationHandlers(
      { successMessage: "Parent created.", errorMessage: "Failed to create parent." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["parents"] }) },
    ),
  });
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    phone: "",
  });

  const handleCreate = async () => {
    await createParent.mutateAsync({
      name: form.name.trim(),
      email: form.email.trim(),
      password: form.password,
      phone: form.phone.trim() || undefined,
    });
    setOpen(false);
    setForm({ name: "", email: "", password: "", phone: "" });
  };

  return (
    <DataListPage
      title="Parents"
      description="Guardian accounts and child links."
      isLoading={isLoading}
      error={error}
      isEmpty={parents.length === 0}
      emptyTitle="No parents"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Parent</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Parent</DialogTitle>
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
                  value={form.password}
                  onChange={(e) =>
                    setForm({ ...form, password: e.target.value })
                  }
                />
              </div>
              <div className="space-y-1">
                <Label>Phone</Label>
                <Input
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
              </div>
              <Button onClick={handleCreate} disabled={createParent.isPending}>
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
            <TableHead>Name</TableHead>
            <TableHead>Phone</TableHead>
            <TableHead>Linked students</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {parents.map((p, index) => (
            <TableRow key={p.id}>
              <TableSerialCell index={index} />
              <TableCell>{p.name}</TableCell>
              <TableCell>{p.phone ?? "—"}</TableCell>
              <TableCell>{p.linked_student_ids.length}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
