import { cn } from "@/lib/utils";

export type FlowStep = {
  label: string;
  sublabel?: string;
  accent?: "default" | "db" | "ml" | "ui";
};

const ACCENT_CLASSES: Record<NonNullable<FlowStep["accent"]>, string> = {
  default: "border-border bg-card",
  db: "border-blue-200/80 bg-blue-50/80 dark:border-blue-900 dark:bg-blue-950/40",
  ml: "border-violet-200/80 bg-violet-50/80 dark:border-violet-900 dark:bg-violet-950/40",
  ui: "border-emerald-200/80 bg-emerald-50/80 dark:border-emerald-900 dark:bg-emerald-950/40",
};

interface VerticalFlowProps {
  steps: FlowStep[];
  className?: string;
  compact?: boolean;
}

export function VerticalFlow({ steps, className, compact }: VerticalFlowProps) {
  return (
    <div className={cn("flex flex-col items-center gap-0", className)}>
      {steps.map((step, index) => (
        <div key={`${step.label}-${index}`} className="flex flex-col items-center">
          <div
            className={cn(
              "w-full max-w-md rounded-lg border px-4 text-center shadow-sm",
              compact ? "py-2" : "py-3",
              ACCENT_CLASSES[step.accent ?? "default"],
            )}
          >
            <p className={cn("font-medium", compact ? "text-sm" : "text-base")}>
              {step.label}
            </p>
            {step.sublabel && (
              <p className="mt-0.5 text-xs text-muted-foreground">{step.sublabel}</p>
            )}
          </div>
          {index < steps.length - 1 && (
            <div
              className="flex h-8 flex-col items-center justify-center text-muted-foreground"
              aria-hidden
            >
              <span className="h-4 w-px bg-border" />
              <span className="text-lg leading-none">↓</span>
              <span className="h-4 w-px bg-border" />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
