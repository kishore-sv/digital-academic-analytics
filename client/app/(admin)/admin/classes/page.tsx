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
import { formatYearNumber } from "@/lib/academic-display";
import { usePrograms } from "@/hooks/use-academic";
import {
  useBatches,
  useClassGroups,
  useCreateClassGroup,
} from "@/hooks/use-academic-structure";

export default function AdminClassesPage() {
  const { data: programData } = usePrograms();
  const programs = programData?.data ?? [];
  const [programId, setProgramId] = useState("");
  const pid = programId || programs[0]?.id || "";
  const { data: batchData } = useBatches(pid);
  const batches = batchData?.data ?? [];
  const [batchId, setBatchId] = useState("");
  const bid = batchId || batches[0]?.id || "";
  const { data: cgData, isLoading, error } = useClassGroups(bid);
  const classGroups = cgData?.data ?? [];
  const createCg = useCreateClassGroup();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ year_number: "1", code: "", name: "" });

  const handleCreate = async () => {
    if (!bid) return;
    await createCg.mutateAsync({
      batch_id: bid,
      year_number: Number(form.year_number),
      code: form.code.trim() || `Y${form.year_number}`,
      name: form.name.trim() || `Year ${form.year_number}`,
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Class Groups"
      description="Year-of-study groups within a batch."
      isLoading={isLoading}
      error={error}
      isEmpty={classGroups.length === 0}
      emptyTitle="No class groups"
    >
      <div className="mb-4 flex flex-wrap gap-3">
        <Select value={pid} onValueChange={(v) => setProgramId(v ?? "")}>
          <SelectTrigger className="w-56">
            <SelectValue placeholder="Program" />
          </SelectTrigger>
          <SelectContent>
            {programs.map((p) => (
              <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={bid} onValueChange={(v) => setBatchId(v ?? "")}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Batch" />
          </SelectTrigger>
          <SelectContent>
            {batches.map((b) => (
              <SelectItem key={b.id} value={b.id}>{b.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Class</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Class Group</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Year number</Label>
                <Input
                  type="number"
                  min={1}
                  max={8}
                  value={form.year_number}
                  onChange={(e) =>
                    setForm({ ...form, year_number: e.target.value })
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
              <Button onClick={handleCreate} disabled={createCg.isPending}>
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
            <TableHead>Year</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {classGroups.map((cg, index) => (
            <TableRow key={cg.id}>
              <TableSerialCell index={index} />
              <TableCell>{cg.code}</TableCell>
              <TableCell>{cg.name}</TableCell>
              <TableCell>{formatYearNumber(cg.year_number)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
