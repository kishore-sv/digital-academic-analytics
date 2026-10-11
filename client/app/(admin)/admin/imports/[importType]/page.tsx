"use client";

import Link from "next/link";
import { notFound } from "next/navigation";
import { use } from "react";
import { ImportWorkflow } from "@/components/imports/import-workflow";
import { Button } from "@/components/ui/button";
import { getImportTypeByKey } from "@/lib/import-types";
import { ROUTES } from "@/lib/constants";

export default function ImportTypeWorkflowPage({
  params,
}: {
  params: Promise<{ importType: string }>;
}) {
  const { importType } = use(params);
  const definition = getImportTypeByKey(importType);

  if (!definition) {
    notFound();
  }

  if (definition.status === "coming_soon") {
    return (
      <div className="space-y-4">
        <p className="text-muted-foreground">
          {definition.title} import is not available yet.
        </p>
        <Button render={<Link href={ROUTES.admin.imports} />}>
          Back to Import Center
        </Button>
      </div>
    );
  }

  return <ImportWorkflow definition={definition} />;
}
