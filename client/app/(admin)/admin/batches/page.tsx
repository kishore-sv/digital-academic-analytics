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
import { usePrograms } from "@/hooks/use-academic";
import { useBatches, useCreateBatch } from "@/hooks/use-academic-structure";

export default function AdminBatchesPage() {
  const { data: programData } = usePrograms();
  const programs = programData?.data ?? [];
  const [programId, setProgramId] = useState("");
  const { data: batchData, isLoading, error } = useBatches(programId || programs[0]?.id);
  const batches = batchData?.data ?? [];
  const createBatch = useCreateBatch();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    program_id: "",
    admission_year: String(new Date().getFullYear()),
    code: "",
    name: "",
  });

  const handleCreate = async () => {
    const pid = form.program_id || programId || programs[0]?.id;
    if (!pid) return;
    await createBatch.mutateAsync({
      program_id: pid,
      admission_year: Number(form.admission_year),
      code: form.code.trim() || form.admission_year,
      name: form.name.trim() || `Batch ${form.admission_year}`,
      is_active: true,
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Batches"
      description="Admission cohorts per program."
      isLoading={isLoading}
      error={error}
      isEmpty={batches.length === 0}
      emptyTitle="No batches"
    >
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <Select
          value={programId || programs[0]?.id || ""}
          onValueChange={(v) => setProgramId(v ?? "")}
        >
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
          <DialogTrigger render={<Button />}>Add Batch</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Batch</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Program</Label>
                <Select
                  value={form.program_id || programId || programs[0]?.id || ""}
                  onValueChange={(v) => setForm({ ...form, program_id: v ?? "" })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Program" />
                  </SelectTrigger>
                  <SelectContent>
                    {programs.map((p) => (
                      <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <Label>Admission year</Label>
                <Input
                  type="number"
                  value={form.admission_year}
                  onChange={(e) =>
                    setForm({ ...form, admission_year: e.target.value })
                  }
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
                <Label>Name</Label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <Button onClick={handleCreate} disabled={createBatch.isPending}>
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
            <TableHead>Admission year</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {batches.map((b, index) => (
            <TableRow key={b.id}>
              <TableSerialCell index={index} />
              <TableCell>{b.code}</TableCell>
              <TableCell>{b.name}</TableCell>
              <TableCell>{b.admission_year}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
