"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PageHeader } from "@/components/layout/page-header";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ImportTypeDefinition } from "@/lib/import-types";
import { ROUTES } from "@/lib/constants";
import {
  downloadImportTemplate,
  getImportErrorsUrl,
  useCommitImport,
  useImportPreview,
  useSaveImportMapping,
  useUploadImport,
  useValidateImport,
} from "@/hooks/use-master-import";

const STEPS = [
  "Choose file",
  "Column mapping",
  "Validation",
  "Preview",
  "Confirm",
  "Result",
] as const;

interface ImportWorkflowProps {
  definition: ImportTypeDefinition;
}

export function ImportWorkflow({ definition }: ImportWorkflowProps) {
  const [step, setStep] = useState(0);
  const [jobId, setJobId] = useState<string | null>(null);
  const [headers, setHeaders] = useState<string[]>([]);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [canonicalFields, setCanonicalFields] = useState<string[]>(
    () => [],
  );
  const [validation, setValidation] = useState<{
    total_rows: number;
    valid_rows: number;
    invalid_rows: number;
    duplicate_rows: number;
    errors: { row: number; message: string }[];
  } | null>(null);

  const upload = useUploadImport();
  const saveMapping = useSaveImportMapping();
  const validate = useValidateImport();
  const commit = useCommitImport();
  const { data: preview } = useImportPreview(
    step >= 3 && jobId ? jobId : undefined,
  );

  const fieldOptions = useMemo(() => {
    const set = new Set([
      ...canonicalFields,
      ...Object.values(mapping).filter(Boolean),
    ]);
    return Array.from(set).sort();
  }, [canonicalFields, mapping]);

  async function handleFileChange(file: File | null) {
    if (!file) return;
    const result = await upload.mutateAsync({
      file,
      importType: definition.apiType,
    });
    setJobId(result.job_id);
    setHeaders(result.detected_headers);
    setMapping(result.suggested_mapping);
    setCanonicalFields(result.canonical_fields);
    setStep(1);
  }

  async function handleDownloadTemplate(format: "csv" | "xlsx") {
    const blob = await downloadImportTemplate(definition.apiType, format);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${definition.key}-template.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function runValidate() {
    if (!jobId) return;
    await saveMapping.mutateAsync({ jobId, mapping });
    const result = await validate.mutateAsync(jobId);
    setValidation(result);
    setStep(2);
  }

  async function runCommit() {
    if (!jobId) return;
    await commit.mutateAsync(jobId);
    setStep(5);
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={`${definition.title} Import`}
        description={
          definition.dependsOn?.length
            ? `Upload a CSV or XLSX file, map columns, validate, and confirm. Requires: ${definition.dependsOn.join(", ")}.`
            : "Upload a CSV or XLSX file, map columns, validate, and confirm."
        }
      />
      {definition.workflowNote && (
        <Alert>
          <AlertDescription>{definition.workflowNote}</AlertDescription>
        </Alert>
      )}
      <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
        {STEPS.map((label, i) => (
          <span
            key={label}
            className={
              i === step
                ? "font-medium text-foreground"
                : i < step
                  ? "text-foreground"
                  : ""
            }
          >
            {i + 1}. {label}
          </span>
        ))}
      </div>

      {step === 0 && (
        <div className="space-y-4 rounded-lg border p-6">
          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => handleDownloadTemplate("csv")}
            >
              Download CSV template
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleDownloadTemplate("xlsx")}
            >
              Download XLSX template
            </Button>
          </div>
          <div className="space-y-2">
            <Label htmlFor="import-file">Upload file</Label>
            <Input
              id="import-file"
              type="file"
              accept=".csv,.xlsx"
              onChange={(e) =>
                handleFileChange(e.target.files?.[0] ?? null)
              }
              disabled={upload.isPending}
            />
          </div>
        </div>
      )}

      {step === 1 && jobId && (
        <div className="space-y-4 rounded-lg border p-6">
          <p className="text-sm text-muted-foreground">
            Map each file column to the expected field.
          </p>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>File column</TableHead>
                <TableHead>Maps to</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {headers.map((header) => (
                <TableRow key={header}>
                  <TableCell>{header}</TableCell>
                  <TableCell>
                    <Select
                      value={mapping[header] ?? ""}
                      onValueChange={(v) =>
                        setMapping((m) => ({ ...m, [header]: v ?? "" }))
                      }
                    >
                      <SelectTrigger className="w-full max-w-xs">
                        <SelectValue placeholder="Select field" />
                      </SelectTrigger>
                      <SelectContent>
                        {fieldOptions.map((f) => (
                          <SelectItem key={f} value={f}>{f}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="flex gap-2">
            <Button onClick={() => setStep(0)} variant="outline">
              Back
            </Button>
            <Button onClick={runValidate} disabled={validate.isPending}>
              Validate
            </Button>
          </div>
        </div>
      )}

      {step === 2 && validation && (
        <div className="space-y-4 rounded-lg border p-6">
          <dl className="grid gap-2 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-muted-foreground">Total rows</dt>
              <dd className="font-medium">{validation.total_rows}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Valid</dt>
              <dd className="font-medium">{validation.valid_rows}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Invalid</dt>
              <dd className="font-medium">{validation.invalid_rows}</dd>
            </div>
            <div>
              <dt className="text-muted-foreground">Duplicates</dt>
              <dd className="font-medium">{validation.duplicate_rows}</dd>
            </div>
          </dl>
          {validation.errors.length > 0 && jobId && (
            <Button variant="outline" render={<a href={getImportErrorsUrl(jobId)} download />}>
              Download error report
            </Button>
          )}
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setStep(1)}>
              Back
            </Button>
            <Button
              onClick={() => setStep(3)}
              disabled={validation.valid_rows === 0}
            >
              Continue to preview
            </Button>
          </div>
        </div>
      )}

      {step === 3 && preview && (
        <div className="space-y-4 rounded-lg border p-6">
          <p className="text-sm">
            <strong>{preview.will_create}</strong> rows will be created.
          </p>
          {preview.sample_rows.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  {Object.keys(preview.sample_rows[0]).map((k) => (
                    <TableHead key={k}>{k}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {preview.sample_rows.slice(0, 5).map((row, i) => (
                  <TableRow key={i}>
                    {Object.values(row).map((v, j) => (
                      <TableCell key={j}>{v}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setStep(2)}>
              Back
            </Button>
            <Button onClick={() => setStep(4)}>Confirm import</Button>
          </div>
        </div>
      )}

      {step === 4 && (
        <div className="space-y-4 rounded-lg border p-6">
          <p className="text-sm text-muted-foreground">
            This will create new records. Duplicate rows are rejected by
            default.
          </p>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setStep(3)}>
              Back
            </Button>
            <Button onClick={runCommit} disabled={commit.isPending}>
              Run import
            </Button>
          </div>
        </div>
      )}

      {step === 5 && (
        <div className="space-y-4 rounded-lg border p-6">
          <p className="font-medium">Import finished.</p>
          <div className="flex flex-wrap gap-2">
            <Button render={<Link href={ROUTES.admin.imports} />}>
              Back to Import Center
            </Button>
            <Button
              variant="outline"
              render={<Link href={ROUTES.admin.importHistory} />}
            >
              View history
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
