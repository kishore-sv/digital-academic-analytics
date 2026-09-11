"use client";

import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/lib/api";
import type { AnalyticsFilters } from "@/types/analytics";
import { useDepartments } from "@/hooks/use-academic";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

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

export function AnalyticsFiltersBar({
  value,
  onChange,
}: {
  value: AnalyticsFilters;
  onChange: (filters: AnalyticsFilters) => void;
}) {
  const { data: deptData } = useDepartments();
  const departments = deptData?.data ?? [];

  const { data: years } = useQuery({
    queryKey: ["academic", "years"],
    queryFn: () => apiFetch<AcademicYear[]>("/academic/years"),
  });

  const defaultYearId =
    years?.find((year) => year.is_current)?.id ?? years?.[0]?.id ?? "";
  const yearId = value.academic_year_id ?? defaultYearId;

  const { data: semesters } = useQuery({
    queryKey: ["academic", "semesters", yearId],
    queryFn: () =>
      apiFetch<Semester[]>(
        yearId
          ? `/academic/semesters?academic_year_id=${yearId}`
          : "/academic/semesters",
      ),
    enabled: Boolean(yearId),
  });

  const yearItems = useMemo(
    () => years?.map((year) => ({ value: year.id, label: year.name })) ?? [],
    [years],
  );

  const semesterItems = useMemo(
    () => [
      { value: "all", label: "All Semesters" },
      ...(semesters?.map((semester) => ({
        value: semester.id,
        label: semester.name,
      })) ?? []),
    ],
    [semesters],
  );

  const departmentItems = useMemo(
    () => [
      { value: "all", label: "All Departments" },
      ...departments.map((department) => ({
        value: department.id,
        label: department.name,
      })),
    ],
    [departments],
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
    <div className="flex flex-wrap gap-3">
      {yearId ? (
        <Select
          items={yearItems}
          value={yearId}
          onValueChange={(selectedYearId) => {
            if (!selectedYearId) return;
            update({ academic_year_id: selectedYearId, semester_id: undefined });
          }}
        >
          <SelectTrigger className="w-auto min-w-48">
            <SelectValue placeholder="Academic Year" />
          </SelectTrigger>
          <SelectContent>
            {years?.map((year) => (
              <SelectItem key={year.id} value={year.id}>{year.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      ) : null}

      <Select
        items={semesterItems}
        value={value.semester_id ?? "all"}
        onValueChange={(selectedSemesterId) =>
          update({
            semester_id:
              !selectedSemesterId || selectedSemesterId === "all"
                ? undefined
                : selectedSemesterId,
          })
        }
      >
        <SelectTrigger className="w-auto min-w-40">
          <SelectValue placeholder="Semester" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Semesters</SelectItem>
          {semesters?.map((semester) => (
            <SelectItem key={semester.id} value={semester.id}>
              {semester.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
        items={departmentItems}
        value={value.department_id ?? "all"}
        onValueChange={(selectedDepartmentId) =>
          update({
            department_id:
              !selectedDepartmentId || selectedDepartmentId === "all"
                ? undefined
                : selectedDepartmentId,
          })
        }
      >
        <SelectTrigger className="w-auto min-w-72 max-w-80">
          <SelectValue placeholder="Department" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Departments</SelectItem>
          {departments.map((department) => (
            <SelectItem key={department.id} value={department.id}>
              {department.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
