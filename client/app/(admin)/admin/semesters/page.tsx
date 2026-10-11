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
import {
  useAcademicYears,
  useCreateSemester,
  useSemesters,
} from "@/hooks/use-academic-structure";

export default function AdminSemestersPage() {
  const { data: years } = useAcademicYears();
  const yearId = years?.find((y) => y.is_current)?.id ?? years?.[0]?.id ?? "";
  const { data: semesters, isLoading, error } = useSemesters(yearId);
  const createSemester = useCreateSemester();
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    academic_year_id: yearId,
    number: "1",
    name: "",
    year_number: "1",
  });

  const yearItems = useMemo(
    () => years?.map((y) => ({ value: y.id, label: y.name })) ?? [],
    [years],
  );

  const handleCreate = async () => {
    await createSemester.mutateAsync({
      academic_year_id: form.academic_year_id || yearId,
      number: Number(form.number),
      name: form.name.trim() || `Semester ${form.number}`,
      year_number: Number(form.year_number),
    });
    setOpen(false);
  };

  const list = semesters ?? [];

  return (
    <DataListPage
      title="Semesters"
      description="Terms within each academic year."
      isLoading={isLoading}
      error={error}
      isEmpty={list.length === 0}
      emptyTitle="No semesters"
    >
      <div className="mb-4 flex justify-end">
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Add Semester</DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add Semester</DialogTitle>
            </DialogHeader>
            <div className="space-y-3">
              <div className="space-y-1">
                <Label>Academic Year</Label>
                <Select
                  value={form.academic_year_id || yearId}
                  onValueChange={(v) =>
                    setForm({ ...form, academic_year_id: v ?? yearId })
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Year" />
                  </SelectTrigger>
                  <SelectContent>
                    {years?.map((y) => (
                      <SelectItem key={y.id} value={y.id}>{y.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1">
                  <Label>Number</Label>
                  <Input
                    type="number"
                    min={1}
                    max={12}
                    value={form.number}
                    onChange={(e) => setForm({ ...form, number: e.target.value })}
                  />
                </div>
                <div className="space-y-1">
                  <Label>Year of study</Label>
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
              </div>
              <div className="space-y-1">
                <Label>Name</Label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Semester 1"
                />
              </div>
              <Button onClick={handleCreate} disabled={createSemester.isPending}>
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
            <TableHead>Number</TableHead>
            <TableHead>Year label</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {list.map((s, index) => (
            <TableRow key={s.id}>
              <TableSerialCell index={index} />
              <TableCell>{s.name}</TableCell>
              <TableCell>{s.number}</TableCell>
              <TableCell>
                {s.year_label ?? formatYearNumber(s.year_number)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </DataListPage>
  );
}
