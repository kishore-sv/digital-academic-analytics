"use client";

import { MASTER_IMPORT_ORDER, OPERATIONAL_IMPORT_ORDER } from "@/lib/import-types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function ImportOrderGuide() {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Recommended import order</CardTitle>
        <CardDescription>
          Import master data in this sequence so dependencies exist before
          dependent records.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ol className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
          {MASTER_IMPORT_ORDER.map((label, index) => (
            <li key={label} className="flex items-center gap-1">
              <span className="font-medium text-foreground">{index + 1}.</span>
              {label}
              {index < MASTER_IMPORT_ORDER.length - 1 && (
                <span className="hidden text-muted-foreground/50 sm:inline">→</span>
              )}
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Suggested operational import order</CardTitle>
        <CardDescription>
          Typical sequence for a semester; dependency validation still applies if
          you import in another order.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ol className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
          {OPERATIONAL_IMPORT_ORDER.map((label, index) => (
            <li key={label} className="flex items-center gap-1">
              <span className="font-medium text-foreground">{index + 1}.</span>
              {label}
              {index < OPERATIONAL_IMPORT_ORDER.length - 1 && (
                <span className="hidden text-muted-foreground/50 sm:inline">→</span>
              )}
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
    </div>
  );
}
