"use client";

import type { SchemaEntity } from "@/lib/architecture/schema-metadata";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

interface EntityDetailDialogProps {
  entity: SchemaEntity | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function EntityDetailDialog({
  entity,
  open,
  onOpenChange,
}: EntityDetailDialogProps) {
  if (!entity) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent
        className="flex max-h-[min(90vh,880px)] w-full flex-col gap-0 overflow-hidden p-0 sm:max-w-3xl lg:max-w-4xl"
      >
        <DialogHeader className="border-b border-border px-6 py-5">
          <DialogTitle className="font-mono text-lg">{entity.tableName}</DialogTitle>
          <DialogDescription>
            SQLAlchemy model: <span className="font-medium">{entity.modelName}</span>
          </DialogDescription>
        </DialogHeader>
        <ScrollArea className="max-h-[calc(min(90vh,880px)-5.5rem)]">
          <div className="space-y-5 px-6 py-5">
            <section>
              <h3 className="text-sm font-semibold">Purpose</h3>
              <p className="mt-1 text-sm text-muted-foreground">{entity.purpose}</p>
            </section>
            <Separator />
            <div className="grid gap-5 sm:grid-cols-2">
              <section>
                <h3 className="text-sm font-semibold">Primary key</h3>
                <p className="mt-1 font-mono text-sm">{entity.primaryKey}</p>
              </section>
              <section>
                <h3 className="text-sm font-semibold">Tenant scope</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {entity.tenantScoped
                    ? "Rows include institution_id (shared database, row-level tenant isolation)."
                    : "Not tenant-scoped via institution_id on this table."}
                </p>
              </section>
            </div>
            <Separator />
            <section>
              <h3 className="text-sm font-semibold">Important columns</h3>
              <ul className="mt-2 grid gap-1 sm:grid-cols-2 lg:grid-cols-3">
                {entity.columns.map((col) => (
                  <li
                    key={col}
                    className="rounded-md bg-muted/50 px-2 py-1 font-mono text-xs text-muted-foreground"
                  >
                    {col}
                  </li>
                ))}
              </ul>
            </section>
            {entity.foreignKeys.length > 0 && (
              <>
                <Separator />
                <section>
                  <h3 className="text-sm font-semibold">Foreign keys</h3>
                  <ul className="mt-2 grid gap-2 sm:grid-cols-2">
                    {entity.foreignKeys.map((fk) => (
                      <li
                        key={fk.column}
                        className="rounded-md border border-border/60 px-3 py-2 text-xs"
                      >
                        <span className="font-mono">{fk.column}</span>
                        <span className="text-muted-foreground"> → {fk.references}</span>
                      </li>
                    ))}
                  </ul>
                </section>
              </>
            )}
            <Separator />
            <section>
              <h3 className="text-sm font-semibold">Relationships</h3>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {entity.relationships.map((rel) => (
                  <Badge key={rel} variant="secondary" className="font-normal">
                    {rel}
                  </Badge>
                ))}
              </div>
            </section>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
