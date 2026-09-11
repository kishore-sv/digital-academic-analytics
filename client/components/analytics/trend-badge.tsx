import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const TREND_STYLES: Record<string, string> = {
  DECLINING:
    "border-red-200 bg-red-100 text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300",
  STABLE:
    "border-yellow-200 bg-yellow-100 text-yellow-800 dark:border-yellow-900 dark:bg-yellow-950 dark:text-yellow-300",
  IMPROVING:
    "border-green-200 bg-green-100 text-green-700 dark:border-green-900 dark:bg-green-950 dark:text-green-300",
};

interface TrendBadgeProps {
  trend: string;
}

export function TrendBadge({ trend }: TrendBadgeProps) {
  const normalized = trend.toUpperCase();
  return (
    <Badge
      variant="outline"
      className={cn(TREND_STYLES[normalized] ?? "text-muted-foreground")}
    >
      {normalized}
    </Badge>
  );
}
