"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ImportOrderGuide } from "@/components/imports/import-order-guide";
import { ImportTypeCard } from "@/components/imports/import-type-card";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ROUTES } from "@/lib/constants";
import {
  IMPORT_TYPE_DEFINITIONS,
  type ImportAvailability,
  type ImportCategory,
} from "@/lib/import-types";
import { useImportSummary } from "@/hooks/use-master-import";

type CategoryFilter = "all" | ImportCategory;
type StatusFilter = "all" | ImportAvailability;

export default function AdminImportsPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState<CategoryFilter>("all");
  const [status, setStatus] = useState<StatusFilter>("all");
  const { data: summary } = useImportSummary();

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return IMPORT_TYPE_DEFINITIONS.filter((t) => {
      if (category !== "all" && t.category !== category) return false;
      if (status !== "all" && t.status !== status) return false;
      if (!q) return true;
      return (
        t.title.toLowerCase().includes(q) ||
        t.description.toLowerCase().includes(q) ||
        t.key.toLowerCase().includes(q)
      );
    });
  }, [search, category, status]);

  const masterCards = filtered.filter((t) => t.category === "master");
  const academicCards = filtered.filter((t) => t.category === "academic");

  const availableCount = IMPORT_TYPE_DEFINITIONS.filter(
    (t) => t.status === "available",
  ).length;
  const comingSoonCount =
    summary?.coming_soon_import_count ??
    IMPORT_TYPE_DEFINITIONS.filter((t) => t.status === "coming_soon").length;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <PageHeader
          title="Academic Data Import Center"
          description="Import institutional academic data using standardized CSV or XLSX files."
        />
        <Button variant="outline" render={<Link href={ROUTES.admin.importHistory} />}>
          Import history
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card size="sm">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Available imports
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-semibold">
              {summary?.available_import_count ?? availableCount}
            </p>
          </CardContent>
        </Card>
        <Card size="sm">
          <CardHeader>
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Coming soon
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-semibold">
              {summary?.coming_soon_import_count ?? comingSoonCount}
            </p>
          </CardContent>
        </Card>
        {summary && summary.total_imports > 0 && (
          <Card size="sm">
            <CardHeader>
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Total imports
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold">{summary.total_imports}</p>
            </CardContent>
          </Card>
        )}
        {summary?.last_import_at && (
          <Card size="sm">
            <CardHeader>
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Last import
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm font-medium">
                {new Date(summary.last_import_at).toLocaleString()}
              </p>
            </CardContent>
          </Card>
        )}
      </div>

      <div className="flex flex-wrap gap-3">
        <Input
          placeholder="Search imports…"
          className="max-w-xs"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Select
          value={category}
          onValueChange={(v) => setCategory((v as CategoryFilter) ?? "all")}
        >
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All categories</SelectItem>
            <SelectItem value="master">Master data</SelectItem>
            <SelectItem value="academic">Academic data</SelectItem>
          </SelectContent>
        </Select>
        <Select
          value={status}
          onValueChange={(v) => setStatus((v as StatusFilter) ?? "all")}
        >
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All statuses</SelectItem>
            <SelectItem value="available">Available</SelectItem>
            <SelectItem value="coming_soon">Coming soon</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <section className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold">Master data</h2>
          <p className="text-sm text-muted-foreground">
            Initial institutional and academic structure used across the system.
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {masterCards.map((d) => (
            <ImportTypeCard key={d.key} definition={d} />
          ))}
        </div>
      </section>

      <section className="space-y-4">
        <div>
          <h2 className="text-lg font-semibold">Academic performance data</h2>
          <p className="text-sm text-muted-foreground">
            Regular academic records imported throughout the year.
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {academicCards.map((d) => (
            <ImportTypeCard key={d.key} definition={d} />
          ))}
        </div>
      </section>

      <ImportOrderGuide />
    </div>
  );
}
