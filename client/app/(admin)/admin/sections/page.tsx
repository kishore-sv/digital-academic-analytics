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
import {
  useBatches,
  useClassGroups,
  useCreateSection,
  useSections,
} from "@/hooks/use-academic-structure";

export default function AdminSectionsPage() {
  const { data: programData } = usePrograms();
  const programs = programData?.data ?? [];
  const [programId, setProgramId] = useState("");
  const pid = programId || programs[0]?.id || "";
  const { data: batchData } = useBatches(pid);
  const batches = batchData?.data ?? [];
  const [batchId, setBatchId] = useState("");
  const bid = batchId || batches[0]?.id || "";
  const { data: cgData } = useClassGroups(bid);
  const classGroups = cgData?.data ?? [];
  const [classGroupId, setClassGroupId] = useState("");
  const cgid = classGroupId || classGroups[0]?.id || "";
  const { data: sectionData, isLoading, error } = useSections(cgid);
  const sections = sectionData?.data ?? [];
  const createSection = useCreateSection();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ code: "A", name: "" });

  const handleCreate = async () => {
    if (!cgid) return;
    await createSection.mutateAsync({
      class_group_id: cgid,
      code: form.code.trim(),
      name: form.name.trim() || `Section ${form.code}`,
      is_active: true,
    });
    setOpen(false);
  };

  return (
    <DataListPage
      title="Sections"
      description="Sections within each class group."
      isLoading={isLoading}
      error={error}
      isEmpty={sections.length === 0}
      emptyTitle="No sections"
    >
      <div className="mb-4 flex flex-wrap gap-3">
        <Select value={pid} onValueChange={(v) => setProgramId(v ?? "")}>
          <SelectTrigger className="w-52">
            <SelectValue placeholder="Program" />
          </SelectTrigger>
          <SelectContent>
            {programs.map((p) => (
              <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={bid} onValueChange={(v) => setBatchId(v ?? "")}>
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Batch" />
          </SelectTrigger>
          <SelectContent>
            {batches.map((b) => (
              <SelectItem key={b.id} value={b.id}>{b.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={cgid} onValueChange={(v) => setClassGroupId(v ?? "")}>
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Class" />
          </SelectTrigger>
          <SelectContent>
            {classGroups.map((cg) => (
              <SelectItem key={cg.id} value={cg.id}>{cg.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Section</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Section</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
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
              <Button onClick={handleCreate} disabled={createSection.isPending}>
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
            <TableHead>Active</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sections.map((s, index) => (
            <TableRow key={s.id}>
              <TableSerialCell index={index} />
              <TableCell>{s.code}</TableCell>
              <TableCell>{s.name}</TableCell>
              <TableCell>{s.is_active ? "Yes" : "No"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
