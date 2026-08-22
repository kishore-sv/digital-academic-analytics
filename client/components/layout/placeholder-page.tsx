import { PageHeader } from "@/components/layout/page-header";
import { Card, CardContent } from "@/components/ui/card";
import type { BreadcrumbItemData } from "@/components/layout/page-breadcrumb";

interface PlaceholderPageProps {
  title: string;
  breadcrumbs: BreadcrumbItemData[];
  description?: string;
}

export function PlaceholderPage({
  title,
  breadcrumbs,
  description,
}: PlaceholderPageProps) {
  return (
    <div className="flex flex-col gap-4">
      <PageHeader
        title={title}
        breadcrumbs={breadcrumbs}
        description={description}
      />
      <Card>
        <CardContent className="pt-6">
          <p className="text-muted-foreground">Coming soon.</p>
        </CardContent>
      </Card>
    </div>
  );
}
