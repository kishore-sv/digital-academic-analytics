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
import { DataListPage } from "@/components/layout/data-list-page";
import { TableSerialCell, TableSerialHead } from "@/components/layout/table-serial";
import {
  useAcademicYears,
  useCreateAcademicYear,
} from "@/hooks/use-academic-structure";
import { apiFetch } from "@/lib/api";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { mergeMutationHandlers } from "@/lib/toast";

export default function AdminAcademicYearsPage() {
  const { data: years, isLoading, error } = useAcademicYears();
  const createYear = useCreateAcademicYear();
  const qc = useQueryClient();
  const setCurrent = useMutation({
    mutationFn: (id: string) =>
      apiFetch(`/academic/years/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_current: true }),
      }),
    ...mergeMutationHandlers(
      { successMessage: "Current academic year updated.", errorMessage: "Update failed." },
      { onSuccess: () => qc.invalidateQueries({ queryKey: ["academic", "years"] }) },
    ),
  });
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");

  const handleCreate = async () => {
    if (!name.trim()) return;
    await createYear.mutateAsync({ name: name.trim(), is_current: false });
    setOpen(false);
    setName("");
  };

  const list = years ?? [];

  return (
    <DataListPage
      title="Academic Years"
      description="Define academic years for your institution."
      isLoading={isLoading}
      error={error}
      isEmpty={list.length === 0}
      emptyTitle="No academic years"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Year</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Academic Year</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Name</Label>
                <Input
                  placeholder="2026-27"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
              <Button onClick={handleCreate} disabled={createYear.isPending}>
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
            <TableHead>Current</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {list.map((y, index) => (
            <TableRow key={y.id}>
              <TableSerialCell index={index} />
              <TableCell>{y.name}</TableCell>
              <TableCell>{y.is_current ? "Yes" : "No"}</TableCell>
              <TableCell className="text-right">
                {!y.is_current && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setCurrent.mutate(y.id)}
                    disabled={setCurrent.isPending}
                  >
                    Set current
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
