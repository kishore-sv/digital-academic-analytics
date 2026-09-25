import type { SchemaEntity } from "@/lib/architecture/schema-metadata";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface EntityCardProps {
  entity: SchemaEntity;
  selected?: boolean;
  onSelect: () => void;
}

export function EntityCard({ entity, selected, onSelect }: EntityCardProps) {
  return (
    <button type="button" onClick={onSelect} className="w-full text-left">
      <Card
        size="sm"
        className={cn(
          "h-full transition-colors hover:border-primary/40 hover:bg-muted/30",
          selected && "border-primary ring-1 ring-primary/30",
        )}
      >
        <CardHeader className="gap-1">
          <div className="flex flex-wrap items-center gap-2">
            <CardTitle className="font-mono text-sm">{entity.tableName}</CardTitle>
            {entity.tenantScoped && (
              <Badge variant="outline" className="text-[10px] font-normal">
                tenant
              </Badge>
            )}
          </div>
          <CardDescription className="line-clamp-2 text-xs">
            {entity.purpose}
          </CardDescription>
        </CardHeader>
      </Card>
    </button>
  );
}
