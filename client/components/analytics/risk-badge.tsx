import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const RISK_VARIANTS: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  LOW: "secondary",
  MEDIUM: "outline",
  HIGH: "destructive",
};

const RISK_STYLES: Record<string, string> = {
  MEDIUM:
    "border-yellow-200 bg-yellow-100 text-yellow-800 dark:border-yellow-900 dark:bg-yellow-950 dark:text-yellow-300",
};

interface RiskBadgeProps {
  level: string;
}

export function RiskBadge({ level }: RiskBadgeProps) {
  const normalized = level.toUpperCase();
  const variant = RISK_VARIANTS[normalized] ?? "default";
  return (
    <Badge variant={variant} className={cn(RISK_STYLES[normalized])}>
      {normalized}
    </Badge>
  );
}
