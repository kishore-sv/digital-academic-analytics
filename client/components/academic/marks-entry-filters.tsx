"use client";

import { useEffect, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAllCourses, useDepartments, usePrograms } from "@/hooks/use-academic";
import {
  useAcademicYears,
  useBatches,
  useClassGroups,
  useProgramCourses,
  useSections,
  useSemesters,
} from "@/hooks/use-academic-structure";
import { useAssessments } from "@/hooks/use-academic-entry";
import {
  applyMarksFilterCascade,
  formatYearOfStudyOption,
  semesterNumbersForYear,
  YEAR_OF_STUDY_OPTIONS,
} from "@/lib/marks-entry-filter-utils";

export interface MarksEntryFilters {
  academic_year_id?: string;
  semester_id?: string;
  department_id?: string;
  year_number?: number;
  program_id?: string;
  batch_id?: string;
  class_group_id?: string;
  section_id?: string;
  course_id?: string;
  assessment_id?: string;
  search?: string;
  date_from?: string;
  date_to?: string;
  attendance_status?: "present" | "absent";
}

const ANY = "any";

interface MarksEntryFiltersBarProps {
  value: MarksEntryFilters;
  onChange: (filters: MarksEntryFilters) => void;
  onApply: () => void;
  onReset: () => void;
  showDepartment?: boolean;
  mode?: "marks" | "attendance";
}

function FilterField({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      <Label className="text-xs font-medium text-muted-foreground">{label}</Label>
      {children}
    </div>
  );
}

export function MarksEntryFiltersBar({
  value,
  onChange,
  onApply,
  onReset,
  showDepartment = true,
  mode = "marks",
}: MarksEntryFiltersBarProps) {
  const { data: years } = useAcademicYears();
  const { data: deptData } = useDepartments();
  const { data: programList } = usePrograms();
  const departments = deptData?.data ?? [];
  const programs = programList?.data ?? [];

  const defaultYearId =
    years?.find((y) => y.is_current)?.id ?? years?.[0]?.id ?? "";
  const yearId = value.academic_year_id ?? defaultYearId;

  const { data: semesters, isLoading: semestersLoading } = useSemesters(yearId);

  const selectedSemester = semesters?.find((s) => s.id === value.semester_id);

  const filteredSemesters = useMemo(() => {
    const list = semesters ?? [];
    if (!value.year_number) return list;
    const allowed = semesterNumbersForYear(value.year_number);
    return list.filter((s) => allowed.includes(s.number));
  }, [semesters, value.year_number]);

  const filteredPrograms = useMemo(
    () =>
      value.department_id
        ? programs.filter((p) => p.department_id === value.department_id)
        : programs,
    [programs, value.department_id],
  );

  const { data: batchData, isLoading: batchesLoading } = useBatches(
    value.program_id,
  );
  const batches = batchData?.data ?? [];

  const classYearNumber =
    value.year_number ?? selectedSemester?.year_number ?? undefined;

  const { data: classGroupData, isLoading: classesLoading } = useClassGroups(
    value.batch_id,
    classYearNumber,
  );
  const classGroups = classGroupData?.data ?? [];

  const { data: sectionData, isLoading: sectionsLoading } = useSections(
    value.class_group_id ?? "",
  );
  const sections = value.class_group_id ? (sectionData?.data ?? []) : [];

  const semesterNumber = selectedSemester?.number;

  const { data: programCourseData } = useProgramCourses(
    value.program_id,
    semesterNumber,
  );
  const curriculumCourseIds = useMemo(() => {
    const rows = programCourseData?.data ?? [];
    if (!value.program_id || rows.length === 0) return null;
    return new Set(rows.map((r) => r.course_id));
  }, [programCourseData?.data, value.program_id]);

  const { data: allCourses = [], isError: coursesError } = useAllCourses();

  const filteredCourses = useMemo(() => {
    let list = allCourses;
    if (value.department_id) {
      list = list.filter((c) => c.department_id === value.department_id);
    }
    if (curriculumCourseIds) {
      list = list.filter((c) => curriculumCourseIds.has(c.id));
    }
    return list;
  }, [allCourses, value.department_id, curriculumCourseIds]);

  const { data: assessmentData, isLoading: assessmentsLoading } = useAssessments(
    value.course_id,
  );
  const assessments = assessmentData?.data ?? [];

  useEffect(() => {
    if (!value.academic_year_id && defaultYearId) {
      onChange({ ...value, academic_year_id: defaultYearId });
    }
  }, [defaultYearId, onChange, value, value.academic_year_id]);

  useEffect(() => {
    if (!value.semester_id || !selectedSemester) return;
    if (value.year_number === selectedSemester.year_number) return;
    onChange(
      applyMarksFilterCascade(value, {
        year_number: selectedSemester.year_number,
      }),
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps -- sync year when semester changes only
  }, [value.semester_id, selectedSemester?.id, selectedSemester?.year_number]);

  function update(partial: Partial<MarksEntryFilters>) {
    onChange(applyMarksFilterCascade(value, partial));
  }

  const courseDisabled = !value.semester_id;
  const assessmentDisabled = !value.course_id;
  const batchDisabled = !value.program_id;
  const classDisabled = !value.batch_id;
  const sectionDisabled = !value.class_group_id;

  return (
    <div className="space-y-4 rounded-lg border bg-card p-4 shadow-sm">
      <div>
        <h2 className="text-sm font-semibold tracking-tight">
          {mode === "attendance" ? "Attendance filters" : "Marks entry filters"}
        </h2>
        <p className="text-xs text-muted-foreground">
          {mode === "attendance"
            ? "Narrow students by academic context, course, and attendance dates. Click Apply filters to load the roster."
            : "Narrow students by academic context, then choose course and assessment. Click Apply filters to load the roster."}
        </p>
      </div>

      <div className="space-y-3">
        <p className="text-xs font-medium uppercase text-muted-foreground">
          Academic context
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <FilterField label="Academic Year">
            <Select
              value={yearId}
              onValueChange={(v) =>
                v && update({ academic_year_id: v, semester_id: undefined })
              }
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select year" />
              </SelectTrigger>
              <SelectContent>
                {years?.map((y) => (
                  <SelectItem key={y.id} value={y.id} label={y.name}>
                    {y.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          <FilterField label="Semester">
            <Select
              value={value.semester_id ?? ANY}
              onValueChange={(v) =>
                update({
                  semester_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger className="w-full" disabled={!yearId || semestersLoading}>
                <SelectValue
                  placeholder={semestersLoading ? "Loading…" : "Any semester"}
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any semester">
                  Any semester
                </SelectItem>
                {filteredSemesters.map((s) => (
                  <SelectItem key={s.id} value={s.id} label={s.name}>
                    {s.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          {showDepartment && (
            <FilterField label="Department">
              <Select
                value={value.department_id ?? ANY}
                onValueChange={(v) =>
                  update({
                    department_id: !v || v === ANY ? undefined : v,
                  })
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Any department" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY} label="Any department">
                    Any department
                  </SelectItem>
                  {departments.map((d) => (
                    <SelectItem key={d.id} value={d.id} label={d.name}>
                      {d.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FilterField>
          )}

          <FilterField label="Year of Study">
            <Select
              value={value.year_number ? String(value.year_number) : ANY}
              onValueChange={(v) => {
                if (!v || v === ANY) {
                  update({ year_number: undefined, semester_id: undefined });
                  return;
                }
                const yearNum = Number(v);
                update({
                  year_number: yearNum,
                  semester_id:
                    selectedSemester &&
                    !semesterNumbersForYear(yearNum).includes(
                      selectedSemester.number,
                    )
                      ? undefined
                      : value.semester_id,
                });
              }}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Any year" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any year">
                  Any year
                </SelectItem>
                {YEAR_OF_STUDY_OPTIONS.map((y) => (
                  <SelectItem
                    key={y}
                    value={String(y)}
                    label={formatYearOfStudyOption(y)}
                  >
                    {formatYearOfStudyOption(y)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>
        </div>
      </div>

      <div className="space-y-3">
        <p className="text-xs font-medium uppercase text-muted-foreground">
          Academic group
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <FilterField label="Program">
            <Select
              value={value.program_id ?? ANY}
              onValueChange={(v) =>
                update({
                  program_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Any program" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any program">
                  Any program
                </SelectItem>
                {filteredPrograms.map((p) => (
                  <SelectItem key={p.id} value={p.id} label={p.name}>
                    {p.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          <FilterField label="Batch">
            <Select
              value={value.batch_id ?? ANY}
              onValueChange={(v) =>
                update({
                  batch_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger
                className="w-full"
                disabled={batchDisabled || batchesLoading}
              >
                <SelectValue
                  placeholder={
                    batchDisabled
                      ? "Select program first"
                      : batchesLoading
                        ? "Loading…"
                        : "Any batch"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any batch">
                  Any batch
                </SelectItem>
                {batches.map((b) => (
                  <SelectItem key={b.id} value={b.id} label={b.name}>
                    {b.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          <FilterField label="Class">
            <Select
              value={value.class_group_id ?? ANY}
              onValueChange={(v) =>
                update({
                  class_group_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger
                className="w-full"
                disabled={classDisabled || classesLoading}
              >
                <SelectValue
                  placeholder={
                    classDisabled
                      ? "Select batch first"
                      : classesLoading
                        ? "Loading…"
                        : "Any class"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any class">
                  Any class
                </SelectItem>
                {classGroups.map((cg) => (
                  <SelectItem key={cg.id} value={cg.id} label={cg.name}>
                    {cg.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          <FilterField label="Section">
            <Select
              value={value.section_id ?? ANY}
              onValueChange={(v) =>
                update({
                  section_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger
                className="w-full"
                disabled={sectionDisabled || sectionsLoading}
              >
                <SelectValue
                  placeholder={
                    sectionDisabled
                      ? "Select class first"
                      : sectionsLoading
                        ? "Loading…"
                        : "Any section"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="Any section">
                  Any section
                </SelectItem>
                {sections.map((s) => (
                  <SelectItem
                    key={s.id}
                    value={s.id}
                    label={`${s.code} — ${s.name}`}
                  >
                    {s.code} — {s.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>
        </div>
      </div>

      <div className="space-y-3">
        <p className="text-xs font-medium uppercase text-muted-foreground">
          {mode === "attendance" ? "Course" : "Assessment"}
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <FilterField label="Course">
            <Select
              value={value.course_id ?? ANY}
              onValueChange={(v) =>
                update({
                  course_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger className="w-full" disabled={courseDisabled}>
                <SelectValue
                  placeholder={
                    courseDisabled
                      ? "Select semester first"
                      : mode === "attendance"
                        ? "Any course"
                        : "Select course"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                {mode === "attendance" && (
                  <SelectItem value={ANY} label="Any course">
                    Any course
                  </SelectItem>
                )}
                {filteredCourses.map((c) => (
                  <SelectItem
                    key={c.id}
                    value={c.id}
                    label={`${c.code} — ${c.name}`}
                  >
                    {c.code} — {c.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>

          {mode === "marks" && (
          <FilterField label="Assessment">
            <Select
              value={value.assessment_id ?? ANY}
              onValueChange={(v) =>
                update({
                  assessment_id: !v || v === ANY ? undefined : v,
                })
              }
            >
              <SelectTrigger
                className="w-full"
                disabled={assessmentDisabled || assessmentsLoading}
              >
                <SelectValue
                  placeholder={
                    assessmentDisabled
                      ? "Select course first"
                      : assessmentsLoading
                        ? "Loading…"
                        : "All assessments"
                  }
                />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ANY} label="All assessments">
                  All assessments
                </SelectItem>
                {assessments.map((a) => (
                  <SelectItem key={a.id} value={a.id} label={a.name}>
                    {a.name} ({a.assessment_type})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FilterField>
          )}

          <FilterField label="Search">
            <Input
              placeholder="Name or roll number"
              value={value.search ?? ""}
              onChange={(e) =>
                update({ search: e.target.value || undefined })
              }
            />
          </FilterField>
        </div>
      </div>

      {mode === "attendance" && (
        <div className="space-y-3">
          <p className="text-xs font-medium uppercase text-muted-foreground">
            Attendance period
          </p>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <FilterField label="Date from">
              <Input
                type="date"
                value={value.date_from ?? ""}
                max={value.date_to || undefined}
                onChange={(e) =>
                  update({ date_from: e.target.value || undefined })
                }
              />
            </FilterField>
            <FilterField label="Date to">
              <Input
                type="date"
                value={value.date_to ?? ""}
                min={value.date_from || undefined}
                onChange={(e) =>
                  update({ date_to: e.target.value || undefined })
                }
              />
            </FilterField>
            <FilterField label="Attendance status">
              <Select
                value={value.attendance_status ?? ANY}
                onValueChange={(v) =>
                  update({
                    attendance_status:
                      !v || v === ANY ? undefined : (v as "present" | "absent"),
                  })
                }
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="All" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ANY} label="All">
                    All
                  </SelectItem>
                  <SelectItem value="present" label="Present">
                    Present
                  </SelectItem>
                  <SelectItem value="absent" label="Absent">
                    Absent
                  </SelectItem>
                </SelectContent>
              </Select>
            </FilterField>
          </div>
        </div>
      )}

      {coursesError && (
        <p className="text-sm text-destructive">
          Could not load courses. Refresh the page or sign in again.
        </p>
      )}

      <div className="flex flex-wrap gap-2 border-t pt-3">
        <Button onClick={onApply}>Apply filters</Button>
        <Button variant="outline" onClick={onReset}>Reset</Button>
      </div>
    </div>
  );
}

export function MarksEntryAppliedSummary({
  filters,
  showDepartment = true,
  inline = false,
}: {
  filters: MarksEntryFilters;
  showDepartment?: boolean;
  inline?: boolean;
}) {
  const { data: years } = useAcademicYears();
  const { data: semesters } = useSemesters(filters.academic_year_id);
  const { data: deptData } = useDepartments();
  const { data: programList } = usePrograms();
  const { data: batchData } = useBatches(filters.program_id);
  const { data: classGroupData } = useClassGroups(
    filters.batch_id,
    filters.year_number,
  );
  const { data: sectionData } = useSections(filters.class_group_id ?? "");
  const { data: courses = [] } = useAllCourses();
  const { data: assessmentData } = useAssessments(filters.course_id);

  const parts = useMemo(() => {
    const labels: string[] = [];
    const year = years?.find((y) => y.id === filters.academic_year_id);
    if (year) labels.push(year.name);
    const sem = semesters?.find((s) => s.id === filters.semester_id);
    if (sem) labels.push(sem.name);
    if (showDepartment && filters.department_id) {
      const dept = deptData?.data?.find((d) => d.id === filters.department_id);
      if (dept) labels.push(dept.name);
    }
    if (filters.year_number) {
      labels.push(formatYearOfStudyOption(filters.year_number));
    }
    if (filters.program_id) {
      const prog = programList?.data?.find((p) => p.id === filters.program_id);
      if (prog) labels.push(prog.name);
    }
    if (filters.batch_id) {
      const batch = batchData?.data?.find((b) => b.id === filters.batch_id);
      if (batch) labels.push(batch.name);
    }
    if (filters.class_group_id) {
      const cg = classGroupData?.data?.find(
        (c) => c.id === filters.class_group_id,
      );
      if (cg) labels.push(cg.name);
    }
    if (filters.section_id) {
      const sec = sectionData?.data?.find((s) => s.id === filters.section_id);
      if (sec) labels.push(`Section ${sec.code}`);
    }
    if (filters.course_id) {
      const course = courses.find((c) => c.id === filters.course_id);
      if (course) labels.push(`${course.code} — ${course.name}`);
    }
    if (filters.assessment_id) {
      const a = assessmentData?.data?.find(
        (x) => x.id === filters.assessment_id,
      );
      if (a) labels.push(a.name);
    }
    if (filters.date_from || filters.date_to) {
      const from = filters.date_from
        ? new Date(`${filters.date_from}T00:00:00`).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
            year: "numeric",
          })
        : "…";
      const to = filters.date_to
        ? new Date(`${filters.date_to}T00:00:00`).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short",
            year: "numeric",
          })
        : "…";
      labels.push(`${from} → ${to}`);
    }
    if (filters.attendance_status === "present") labels.push("Present");
    if (filters.attendance_status === "absent") labels.push("Absent");
    return labels;
  }, [
    filters,
    years,
    semesters,
    deptData?.data,
    programList?.data,
    batchData?.data,
    classGroupData?.data,
    sectionData?.data,
    courses,
    assessmentData?.data,
    showDepartment,
  ]);

  if (parts.length === 0) {
    return inline ? null : null;
  }

  const content = parts.join(" · ");

  if (inline) {
    return <span className="text-muted-foreground">{content}</span>;
  }

  return (
    <div className="rounded-md border bg-muted/40 px-3 py-2">
      <p className="text-xs font-medium text-muted-foreground">Selected context</p>
      <p className="text-sm">{content}</p>
    </div>
  );
}
