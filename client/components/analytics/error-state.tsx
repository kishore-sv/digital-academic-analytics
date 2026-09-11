import { IconAlertCircle } from "@tabler/icons-react";

interface ErrorStateProps {
  title?: string;
  description?: string;
}

export function ErrorState({
  title = "Something went wrong",
  description = "Please try again later.",
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 py-12 text-center text-muted-foreground">
      <IconAlertCircle className="size-8 text-destructive" />
      <p className="font-medium text-foreground">{title}</p>
      <p className="text-sm">{description}</p>
    </div>
  );
}
