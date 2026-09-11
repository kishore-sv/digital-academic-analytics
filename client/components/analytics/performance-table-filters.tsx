"use client";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { SemesterResult } from "@/hooks/use-academic";

export interface PerformanceTableFilters {
  performance_trend?: string;
  backlog_status?: string;
  cgpa_band?: string;
}

interface PerformanceTableFiltersBarProps {
  value: PerformanceTableFilters;
  onChange: (filters: PerformanceTableFilters) => void;
}

const ALL = "all";

export function filterSemesterResults(
  results: SemesterResult[],
  filters: PerformanceTableFilters,
): SemesterResult[] {
  return results.filter((result) => {
    if (
      filters.performance_trend &&
      result.performance_trend !== filters.performance_trend
    ) {
      return false;
    }

    const backlogs = result.backlog_count ?? 0;
    if (filters.backlog_status === "with" && backlogs === 0) return false;
    if (filters.backlog_status === "without" && backlogs > 0) return false;

    const cgpa = result.cgpa;
    if (filters.cgpa_band) {
      if (cgpa == null) return false;
      if (filters.cgpa_band === "low" && cgpa >= 6) return false;
      if (filters.cgpa_band === "medium" && (cgpa < 6 || cgpa > 7.5)) {
        return false;
      }
      if (filters.cgpa_band === "high" && cgpa <= 7.5) return false;
    }

    return true;
  });
}

export function PerformanceTableFiltersBar({
  value,
  onChange,
}: PerformanceTableFiltersBarProps) {
  function update(partial: Partial<PerformanceTableFilters>) {
    onChange({ ...value, ...partial });
  }

  function clearAll() {
    onChange({});
  }

  const hasFilters = Object.values(value).some(
    (v) => v !== undefined && v !== "",
  );

  return (
    <div className="flex flex-wrap gap-3">
      <Select
        value={value.performance_trend ?? ALL}
        onValueChange={(v) =>
          update({ performance_trend: !v || v === ALL ? undefined : v })
        }
      >
        <SelectTrigger className="w-[150px]">
          <SelectValue placeholder="Trend" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={ALL}>All Trends</SelectItem>
          <SelectItem value="IMPROVING">Improving</SelectItem>
          <SelectItem value="STABLE">Stable</SelectItem>
          <SelectItem value="DECLINING">Declining</SelectItem>
        </SelectContent>
      </Select>

      <Select
        value={value.backlog_status ?? ALL}
        onValueChange={(v) =>
          update({ backlog_status: !v || v === ALL ? undefined : v })
        }
      >
        <SelectTrigger className="w-[160px]">
          <SelectValue placeholder="Backlogs" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={ALL}>All Students</SelectItem>
          <SelectItem value="with">Has Backlogs</SelectItem>
          <SelectItem value="without">No Backlogs</SelectItem>
        </SelectContent>
      </Select>

      <Select
        value={value.cgpa_band ?? ALL}
        onValueChange={(v) =>
          update({ cgpa_band: !v || v === ALL ? undefined : v })
        }
      >
        <SelectTrigger className="w-[150px]">
          <SelectValue placeholder="CGPA" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value={ALL}>All CGPA</SelectItem>
          <SelectItem value="low">Below 6.0</SelectItem>
          <SelectItem value="medium">6.0 – 7.5</SelectItem>
          <SelectItem value="high">Above 7.5</SelectItem>
        </SelectContent>
      </Select>

      {hasFilters && (
        <Button variant="ghost" size="sm" onClick={clearAll}>
          Clear filters
        </Button>
      )}
    </div>
  );
}
