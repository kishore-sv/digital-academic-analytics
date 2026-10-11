"use client";

import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import type { ImportTypeDefinition } from "@/lib/import-types";
import { importWorkflowHref } from "@/lib/import-types";
import { IconChevronDown } from "@tabler/icons-react";

interface ImportTypeCardProps {
  definition: ImportTypeDefinition;
}

export function ImportTypeCard({ definition }: ImportTypeCardProps) {
  const Icon = definition.icon;
  const available = definition.status === "available";
  const formats = definition.formats.join(" / ");

  return (
    <Card className="flex h-full flex-col">
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
            <Icon className="size-5 text-muted-foreground" aria-hidden />
          </div>
          <Badge variant={available ? "default" : "secondary"}>
            {available ? "Available" : "Coming Soon"}
          </Badge>
        </div>
        <CardTitle className="text-base">{definition.title}</CardTitle>
        <CardDescription className="line-clamp-3">
          {definition.description}
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 space-y-2 text-xs text-muted-foreground">
        <p>{formats}</p>
        {definition.dependsOn && definition.dependsOn.length > 0 && (
          <Collapsible>
            <CollapsibleTrigger className="flex items-center gap-1 text-xs font-medium text-foreground hover:underline">
              Dependencies
              <IconChevronDown className="size-3.5" />
            </CollapsibleTrigger>
            <CollapsibleContent className="pt-1">
              <ul className="list-inside list-disc space-y-0.5">
                {definition.dependsOn.map((d) => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            </CollapsibleContent>
          </Collapsible>
        )}
      </CardContent>
      <CardFooter>
        {available ? (
          <Button render={<Link href={importWorkflowHref(definition.key)} />} className="w-full">
            Import Now
          </Button>
        ) : (
          <Button className="w-full" disabled>
            Coming Soon
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
