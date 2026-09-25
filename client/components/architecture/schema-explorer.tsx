"use client";

import { useMemo, useState } from "react";
import { EntityCard } from "@/components/architecture/entity-card";
import { EntityDetailDialog } from "@/components/architecture/entity-detail-dialog";
import { Input } from "@/components/ui/input";
import { SCHEMA_ENTITIES, type SchemaEntity } from "@/lib/architecture/schema-metadata";

export function SchemaExplorer() {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<SchemaEntity | null>(null);
  const [sheetOpen, setSheetOpen] = useState(false);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return SCHEMA_ENTITIES;
    return SCHEMA_ENTITIES.filter(
      (e) =>
        e.tableName.includes(q) ||
        e.modelName.toLowerCase().includes(q) ||
        e.purpose.toLowerCase().includes(q),
    );
  }, [query]);

  function openEntity(entity: SchemaEntity) {
    setSelected(entity);
    setSheetOpen(true);
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-lg font-semibold">Database schema</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          {SCHEMA_ENTITIES.length} tables from the current SQLAlchemy models. Click a
          card for column and relationship details (read-only).
        </p>
      </div>
      <Input
        placeholder="Filter tables…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="max-w-md"
      />
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((entity) => (
          <EntityCard
            key={entity.tableName}
            entity={entity}
            selected={selected?.tableName === entity.tableName}
            onSelect={() => openEntity(entity)}
          />
        ))}
      </div>
      <EntityDetailDialog
        entity={selected}
        open={sheetOpen}
        onOpenChange={setSheetOpen}
      />
    </div>
  );
}
