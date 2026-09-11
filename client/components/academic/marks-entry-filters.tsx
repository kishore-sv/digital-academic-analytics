"use client";

import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { apiFetch } from "@/lib/api";
import { useCourses, useDepartments, usePrograms } from "@/hooks/use-academic";

export interface MarksEntryFilters {
  academic_year_id?: string;
  semester_id?: string;
  department_id?: string;
  program_id?: string;
  course_id?: string;
  section?: string;
  search?: string;
}

interface AcademicYear {
  id: string;
  name: string;
  is_current: boolean;
}

interface Semester {
  id: string;
  academic_year_id: string;
  number: number;
  name: string;
}

const ALL = "all";
const SECTIONS = ["CSE-A", "CSE-B", "ECE-A", "ECE-B", "IST-A", "IST-B"];

interface MarksEntryFiltersBarProps {
  value: MarksEntryFilters;
  onChange: (filters: MarksEntryFilters) => void;
  onApply: () => void;
  onReset: () => void;
  showDepartment?: boolean;
}

export function MarksEntryFiltersBar({
  value,
  onChange,
  onApply,
  onReset,
  showDepartment = true,
}: MarksEntryFiltersBarProps) {
  const { data: deptData } = useDepartments();
  const { data: programList } = usePrograms();
  const departments = deptData?.data ?? [];
  const programs = programList?.data ?? [];

  const { data: years } = useQuery({
    queryKey: ["academic", "years"],
    queryFn: () => apiFetch<AcademicYear[]>("/academic/years"),
  });

  const defaultYearId =
    years?.find((y) => y.is_current)?.id ?? years?.[0]?.id ?? "";
  const yearId = value.academic_year_id ?? defaultYearId;

  const { data: semesters } = useQuery({
    queryKey: ["academic", "semesters", yearId],
    queryFn: () =>
      apiFetch<Semester[]>(
        yearId ? `/academic/semesters?academic_year_id=${yearId}` : "/academic/semesters",
      ),
    enabled: Boolean(yearId),
  });

  const { data: coursesData } = useCourses(1, 200);
  const allCourses = coursesData?.data ?? [];

  const filteredCourses = useMemo(() => {
    let list = allCourses;
    if (value.department_id) {
      list = list.filter((c) => c.department_id === value.department_id);
    }
    return list;
  }, [allCourses, value.department_id]);

  const filteredPrograms = useMemo(
    () =>
      value.department_id
        ? programs.filter((p) => p.department_id === value.department_id)
        : programs,
    [programs, value.department_id],
  );

  const yearItems = useMemo(
    () => years?.map((y) => ({ value: y.id, label: y.name })) ?? [],
    [years],
  );
  const semesterItems = useMemo(
    () => semesters?.map((s) => ({ value: s.id, label: s.name })) ?? [],
    [semesters],
  );
  const deptItems = useMemo(
    () => [
      { value: ALL, label: "All Departments" },
      ...departments.map((d) => ({ value: d.id, label: d.name })),
    ],
    [departments],
  );
  const programItems = useMemo(
    () => [
      { value: ALL, label: "All Programs" },
      ...filteredPrograms.map((p) => ({ value: p.id, label: p.name })),
    ],
    [filteredPrograms],
  );
  const courseItems = useMemo(
    () => filteredCourses.map((c) => ({ value: c.id, label: `${c.code} — ${c.name}` })),
    [filteredCourses],
  );
  const sectionItems = useMemo(
    () => [
      { value: ALL, label: "All Sections" },
      ...SECTIONS.map((s) => ({ value: s, label: s })),
    ],
    [],
  );

  useEffect(() => {
    if (!value.academic_year_id && defaultYearId) {
      onChange({ ...value, academic_year_id: defaultYearId });
    }
  }, [defaultYearId, value, onChange, value.academic_year_id]);

  function update(partial: Partial<MarksEntryFilters>) {
    onChange({ ...value, ...partial });
  }

  return (
    <div className="space-y-3 rounded-lg border p-4">
      <div className="flex flex-wrap gap-3">
        {yearId && (
          <Select
            items={yearItems}
            value={yearId}
            onValueChange={(v) => v && update({ academic_year_id: v, semester_id: undefined })}
          >
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Academic Year" />
            </SelectTrigger>
            <SelectContent>
              {years?.map((y) => (
                <SelectItem key={y.id} value={y.id}>{y.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
        <Select
          items={semesterItems}
          value={value.semester_id ?? ""}
          onValueChange={(v) => update({ semester_id: v || undefined })}
        >
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Semester" />
          </SelectTrigger>
          <SelectContent>
            {semesters?.map((s) => (
              <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        {showDepartment && (
          <Select
            items={deptItems}
            value={value.department_id ?? ALL}
            onValueChange={(v) =>
              update({
                department_id: !v || v === ALL ? undefined : v,
                program_id: undefined,
                course_id: undefined,
              })
            }
          >
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Department" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={ALL}>All Departments</SelectItem>
              {departments.map((d) => (
                <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
        <Select
          items={programItems}
          value={value.program_id ?? ALL}
          onValueChange={(v) => update({ program_id: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-44">
            <SelectValue placeholder="Program" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Programs</SelectItem>
            {filteredPrograms.map((p) => (
              <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          items={courseItems}
          value={value.course_id ?? ""}
          onValueChange={(v) => update({ course_id: v || undefined })}
        >
          <SelectTrigger className="w-56">
            <SelectValue placeholder="Course / Subject" />
          </SelectTrigger>
          <SelectContent>
            {filteredCourses.map((c) => (
              <SelectItem key={c.id} value={c.id}>{c.code} — {c.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          items={sectionItems}
          value={value.section ?? ALL}
          onValueChange={(v) => update({ section: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-36">
            <SelectValue placeholder="Section" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Sections</SelectItem>
            {SECTIONS.map((s) => (
              <SelectItem key={s} value={s}>{s}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Input
          placeholder="Search by name / reg no"
          className="w-52"
          value={value.search ?? ""}
          onChange={(e) => update({ search: e.target.value || undefined })}
        />
      </div>
      <div className="flex gap-2">
        <Button onClick={onApply}>Apply Filters</Button>
        <Button variant="outline" onClick={onReset}>Reset</Button>
      </div>
    </div>
  );
}
