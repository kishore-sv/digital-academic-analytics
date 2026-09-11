import { Spinner } from "@/components/ui/spinner";
import { cn } from "@/lib/utils";

interface LoadingStateProps {
  message?: string;
  className?: string;
  compact?: boolean;
}

export function LoadingState({
  message = "Loading...",
  className,
  compact = false,
}: LoadingStateProps) {
  return (
    <div
      className={cn(
        "flex items-center justify-center gap-2 text-muted-foreground",
        compact ? "py-6" : "py-12",
        className,
      )}
    >
      <Spinner className="size-5" />
      <span>{message}</span>
    </div>
  );
}
