"use client";

import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { apiFetch } from "@/lib/api";
import { useCourses, useDepartments, usePrograms } from "@/hooks/use-academic";
import type { AnalyticsFilters } from "@/types/analytics";

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

const RISK_LEVEL_ITEMS = [
  { value: ALL, label: "All Risk Levels" },
  { value: "LOW", label: "Low" },
  { value: "MEDIUM", label: "Medium" },
  { value: "HIGH", label: "High" },
];

interface ReportFiltersBarProps {
  value: AnalyticsFilters;
  onChange: (filters: AnalyticsFilters) => void;
  onApply: () => void;
  onReset: () => void;
}

export function ReportFiltersBar({
  value,
  onChange,
  onApply,
  onReset,
}: ReportFiltersBarProps) {
  const { data: deptData } = useDepartments();
  const { data: programList } = usePrograms();
  const { data: courseData } = useCourses(1, 200);
  const departments = deptData?.data ?? [];
  const programs = programList?.data ?? [];
  const courses = courseData?.data ?? [];

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

  const yearItems = useMemo(
    () => years?.map((y) => ({ value: y.id, label: y.name })) ?? [],
    [years],
  );

  const semesterItems = useMemo(
    () => [
      { value: ALL, label: "All Semesters" },
      ...(semesters?.map((s) => ({ value: s.id, label: s.name })) ?? []),
    ],
    [semesters],
  );

  const departmentItems = useMemo(
    () => [
      { value: ALL, label: "All Departments" },
      ...departments.map((d) => ({ value: d.id, label: d.name })),
    ],
    [departments],
  );

  const filteredPrograms = useMemo(
    () =>
      value.department_id
        ? programs.filter((p) => p.department_id === value.department_id)
        : programs,
    [programs, value.department_id],
  );

  const programItems = useMemo(
    () => [
      { value: ALL, label: "All Programs" },
      ...filteredPrograms.map((p) => ({ value: p.id, label: p.name })),
    ],
    [filteredPrograms],
  );

  const filteredCourses = useMemo(
    () =>
      value.department_id
        ? courses.filter((c) => c.department_id === value.department_id)
        : courses,
    [courses, value.department_id],
  );

  const courseItems = useMemo(
    () => [
      { value: ALL, label: "All Courses" },
      ...filteredCourses.map((c) => ({
        value: c.id,
        label: `${c.code} — ${c.name}`,
      })),
    ],
    [filteredCourses],
  );

  useEffect(() => {
    if (!value.academic_year_id && defaultYearId) {
      onChange({ ...value, academic_year_id: defaultYearId });
    }
  }, [defaultYearId, value, onChange, value.academic_year_id]);

  function update(partial: Partial<AnalyticsFilters>) {
    onChange({ ...value, ...partial });
  }

  return (
    <div className="space-y-3 rounded-lg border p-4">
      <h3 className="text-sm font-semibold">Generate Academic Report</h3>
      <div className="flex flex-wrap gap-3">
        {yearId && (
          <Select
            items={yearItems}
            value={yearId}
            onValueChange={(v) => v && update({ academic_year_id: v, semester_id: undefined })}
          >
            <SelectTrigger className="w-[180px]">
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
          value={value.semester_id ?? ALL}
          onValueChange={(v) => update({ semester_id: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-[160px]">
            <SelectValue placeholder="Semester" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Semesters</SelectItem>
            {semesters?.map((s) => (
              <SelectItem key={s.id} value={s.id}>{s.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          items={departmentItems}
          value={value.department_id ?? ALL}
          onValueChange={(v) =>
            update({
              department_id: !v || v === ALL ? undefined : v,
              program_id: undefined,
              course_id: undefined,
            })
          }
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Department" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Departments</SelectItem>
            {departments.map((d) => (
              <SelectItem key={d.id} value={d.id}>{d.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          items={programItems}
          value={value.program_id ?? ALL}
          onValueChange={(v) => update({ program_id: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-[180px]">
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
          value={value.course_id ?? ALL}
          onValueChange={(v) => update({ course_id: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Course" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Courses</SelectItem>
            {filteredCourses.map((c) => (
              <SelectItem key={c.id} value={c.id}>{c.code} — {c.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          items={RISK_LEVEL_ITEMS}
          value={value.risk_level ?? ALL}
          onValueChange={(v) => update({ risk_level: !v || v === ALL ? undefined : v })}
        >
          <SelectTrigger className="w-[150px]">
            <SelectValue placeholder="Risk Level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Risk Levels</SelectItem>
            <SelectItem value="LOW">Low</SelectItem>
            <SelectItem value="MEDIUM">Medium</SelectItem>
            <SelectItem value="HIGH">High</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="flex gap-2">
        <Button onClick={onApply}>Apply Filters</Button>
        <Button variant="outline" onClick={onReset}>Reset</Button>
      </div>
    </div>
  );
}

export function filtersFromSearchParams(params: URLSearchParams): AnalyticsFilters {
  const filters: AnalyticsFilters = {};
  for (const key of [
    "academic_year_id",
    "semester_id",
    "department_id",
    "program_id",
    "course_id",
    "risk_level",
  ] as const) {
    const val = params.get(key);
    if (val) filters[key] = val;
  }
  return filters;
}

export function filtersToSearchParams(filters: AnalyticsFilters): URLSearchParams {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) params.set(key, value);
  }
  return params;
}
