"use client";

import { useEffect, useMemo } from "react";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useDepartments, usePrograms } from "@/hooks/use-academic";
import {
  useAcademicYears,
  useBatches,
  useClassGroups,
  useSections,
  useSemesters,
} from "@/hooks/use-academic-structure";
import { formatYearNumber } from "@/lib/academic-display";

export interface StudentPlacementValue {
  department_id: string;
  program_id: string;
  batch_id: string;
  class_group_id: string;
  section_id: string;
  current_semester_id: string;
}

interface StudentPlacementSelectorsProps {
  value: StudentPlacementValue;
  onChange: (value: StudentPlacementValue) => void;
}

export function StudentPlacementSelectors({
  value,
  onChange,
}: StudentPlacementSelectorsProps) {
  const { data: deptData } = useDepartments();
  const departments = deptData?.data ?? [];
  const { data: programData } = usePrograms();
  const programs = useMemo(
    () =>
      (programData?.data ?? []).filter(
        (p) => !value.department_id || p.department_id === value.department_id,
      ),
    [programData?.data, value.department_id],
  );
  const { data: batchData } = useBatches(value.program_id || undefined);
  const batches = batchData?.data ?? [];
  const { data: yearData } = useAcademicYears();
  const currentYear =
    yearData?.find((y) => y.is_current) ?? yearData?.[0] ?? null;
  const { data: semesters } = useSemesters(currentYear?.id);
  const semesterList = semesters ?? [];
  const selectedSem = semesterList.find((s) => s.id === value.current_semester_id);
  const { data: classGroupData } = useClassGroups(
    value.batch_id || undefined,
    selectedSem?.year_number,
  );
  const classGroups = classGroupData?.data ?? [];
  const { data: sectionData } = useSections(value.class_group_id || undefined);
  const sections = sectionData?.data ?? [];

  useEffect(() => {
    if (!value.department_id && departments[0]) {
      onChange({ ...value, department_id: departments[0].id });
    }
  }, [departments, onChange, value]);

  useEffect(() => {
    if (value.department_id && programs.length === 1 && !value.program_id) {
      onChange({ ...value, program_id: programs[0].id });
    }
  }, [onChange, programs, value]);

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <div className="space-y-1">
        <Label>Department</Label>
        <Select
          value={value.department_id}
          onValueChange={(department_id) =>
            onChange({
              ...value,
              department_id: department_id ?? "",
              program_id: "",
              batch_id: "",
              class_group_id: "",
              section_id: "",
            })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Department" />
          </SelectTrigger>
          <SelectContent>
            {departments.map((d) => (
              <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1">
        <Label>Program</Label>
        <Select
          value={value.program_id}
          onValueChange={(program_id) =>
            onChange({
              ...value,
              program_id: program_id ?? "",
              batch_id: "",
              class_group_id: "",
              section_id: "",
            })
          }
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
        <Label>Batch</Label>
        <Select
          value={value.batch_id}
          onValueChange={(batch_id) =>
            onChange({
              ...value,
              batch_id: batch_id ?? "",
              class_group_id: "",
              section_id: "",
            })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Batch" />
          </SelectTrigger>
          <SelectContent>
            {batches.map((b) => (
              <SelectItem key={b.id} value={b.id}>{b.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1">
        <Label>Current Semester</Label>
        <Select
          value={value.current_semester_id}
          onValueChange={(current_semester_id) =>
            onChange({
              ...value,
              current_semester_id: current_semester_id ?? "",
              class_group_id: "",
              section_id: "",
            })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Semester" />
          </SelectTrigger>
          <SelectContent>
            {semesterList.map((s) => (
              <SelectItem key={s.id} value={s.id}>
                {s.name} ({formatYearNumber(s.year_number)})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1">
        <Label>Class Group</Label>
        <Select
          value={value.class_group_id}
          onValueChange={(class_group_id) =>
            onChange({
              ...value,
              class_group_id: class_group_id ?? "",
              section_id: "",
            })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Class" />
          </SelectTrigger>
          <SelectContent>
            {classGroups.map((cg) => (
              <SelectItem key={cg.id} value={cg.id}>
                {cg.name} ({formatYearNumber(cg.year_number)})
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1">
        <Label>Section</Label>
        <Select
          value={value.section_id}
          onValueChange={(section_id) =>
            onChange({ ...value, section_id: section_id ?? "" })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Section" />
          </SelectTrigger>
          <SelectContent>
            {sections.map((s) => (
              <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
