import { Card, CardContent } from "@/components/ui/card";

interface EmptyStateProps {
  title: string;
  description?: string;
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <Card>
      <CardContent className="py-12 text-center text-muted-foreground">
        <p className="font-medium">{title}</p>
        {description && <p className="text-sm mt-1">{description}</p>}
      </CardContent>
    </Card>
  );
}
