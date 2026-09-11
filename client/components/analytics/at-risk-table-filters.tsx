"use client";

import { useMemo } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export interface AtRiskTableFilters {
  department_name?: string;
  semester?: number;
  risk_level?: string;
  performance_trend?: string;
  attendance_band?: string;
  cgpa_band?: string;
}

interface AtRiskTableFiltersBarProps {
  value: AtRiskTableFilters;
  onChange: (filters: AtRiskTableFilters) => void;
  departments: string[];
  semesters: number[];
}

const ALL = "all";

const RISK_LEVEL_ITEMS = [
  { value: ALL, label: "All Risk Levels" },
  { value: "HIGH", label: "High" },
  { value: "MEDIUM", label: "Medium" },
];

const TREND_ITEMS = [
  { value: ALL, label: "All Trends" },
  { value: "IMPROVING", label: "Improving" },
  { value: "STABLE", label: "Stable" },
  { value: "DECLINING", label: "Declining" },
];

const ATTENDANCE_ITEMS = [
  { value: ALL, label: "All Attendance" },
  { value: "low", label: "Below 60%" },
  { value: "medium", label: "60% – 75%" },
  { value: "high", label: "Above 75%" },
];

const CGPA_ITEMS = [
  { value: ALL, label: "All CGPA" },
  { value: "low", label: "Below 6.0" },
  { value: "medium", label: "6.0 – 7.5" },
  { value: "high", label: "Above 7.5" },
];

export function AtRiskTableFiltersBar({
  value,
  onChange,
  departments,
  semesters,
}: AtRiskTableFiltersBarProps) {
  const departmentItems = useMemo(
    () => [
      { value: ALL, label: "All Departments" },
      ...departments.map((department) => ({
        value: department,
        label: department,
      })),
    ],
    [departments],
  );

  const semesterItems = useMemo(
    () => [
      { value: ALL, label: "All Semesters" },
      ...semesters.map((semester) => ({
        value: String(semester),
        label: `Semester ${semester}`,
      })),
    ],
    [semesters],
  );

  function update(partial: Partial<AtRiskTableFilters>) {
    onChange({ ...value, ...partial });
  }

  function clearAll() {
    onChange({});
  }

  const hasFilters = Object.values(value).some((v) => v !== undefined && v !== "");

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-3">
        <Select
          items={departmentItems}
          value={value.department_name ?? ALL}
          onValueChange={(selected) =>
            update({
              department_name:
                !selected || selected === ALL ? undefined : selected,
            })
          }
        >
          <SelectTrigger className="w-auto min-w-56 max-w-80">
            <SelectValue placeholder="Department" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Departments</SelectItem>
            {departments.map((department) => (
              <SelectItem key={department} value={department}>
                {department}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          items={semesterItems}
          value={value.semester?.toString() ?? ALL}
          onValueChange={(selected) =>
            update({
              semester:
                !selected || selected === ALL ? undefined : parseInt(selected, 10),
            })
          }
        >
          <SelectTrigger className="w-auto min-w-40">
            <SelectValue placeholder="Semester" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={ALL}>All Semesters</SelectItem>
            {semesters.map((semester) => (
              <SelectItem key={semester} value={String(semester)}>
                Semester {semester}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          items={RISK_LEVEL_ITEMS}
          value={value.risk_level ?? ALL}
          onValueChange={(selected) =>
            update({
              risk_level: !selected || selected === ALL ? undefined : selected,
            })
          }
        >
          <SelectTrigger className="w-auto min-w-40">
            <SelectValue placeholder="Risk Level" />
          </SelectTrigger>
          <SelectContent>
            {RISK_LEVEL_ITEMS.map((item) => (
              <SelectItem key={item.value} value={item.value}>
                {item.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          items={TREND_ITEMS}
          value={value.performance_trend ?? ALL}
          onValueChange={(selected) =>
            update({
              performance_trend:
                !selected || selected === ALL ? undefined : selected,
            })
          }
        >
          <SelectTrigger className="w-auto min-w-40">
            <SelectValue placeholder="Trend" />
          </SelectTrigger>
          <SelectContent>
            {TREND_ITEMS.map((item) => (
              <SelectItem key={item.value} value={item.value}>
                {item.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          items={ATTENDANCE_ITEMS}
          value={value.attendance_band ?? ALL}
          onValueChange={(selected) =>
            update({
              attendance_band:
                !selected || selected === ALL ? undefined : selected,
            })
          }
        >
          <SelectTrigger className="w-auto min-w-44">
            <SelectValue placeholder="Attendance" />
          </SelectTrigger>
          <SelectContent>
            {ATTENDANCE_ITEMS.map((item) => (
              <SelectItem key={item.value} value={item.value}>
                {item.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select
          items={CGPA_ITEMS}
          value={value.cgpa_band ?? ALL}
          onValueChange={(selected) =>
            update({
              cgpa_band: !selected || selected === ALL ? undefined : selected,
            })
          }
        >
          <SelectTrigger className="w-auto min-w-40">
            <SelectValue placeholder="CGPA" />
          </SelectTrigger>
          <SelectContent>
            {CGPA_ITEMS.map((item) => (
              <SelectItem key={item.value} value={item.value}>
                {item.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {hasFilters && (
          <Button variant="ghost" size="sm" onClick={clearAll}>
            Clear filters
          </Button>
        )}
      </div>
    </div>
  );
}

export function atRiskFiltersToQuery(filters: AtRiskTableFilters): string {
  const params = new URLSearchParams();
  if (filters.department_name) params.set("department_name", filters.department_name);
  if (filters.semester) params.set("semester", String(filters.semester));
  if (filters.risk_level) params.set("risk_level", filters.risk_level);
  if (filters.performance_trend) params.set("performance_trend", filters.performance_trend);
  if (filters.attendance_band) params.set("attendance_band", filters.attendance_band);
  if (filters.cgpa_band) params.set("cgpa_band", filters.cgpa_band);
  const qs = params.toString();
  return qs ? `&${qs}` : "";
}
