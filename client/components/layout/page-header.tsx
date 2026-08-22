import { PageBreadcrumb, type BreadcrumbItemData } from "./page-breadcrumb";

interface PageHeaderProps {
  title: string;
  breadcrumbs: BreadcrumbItemData[];
  description?: string;
}

export function PageHeader({ title, breadcrumbs, description }: PageHeaderProps) {
  return (
    <div className="flex flex-col gap-2">
      <PageBreadcrumb items={breadcrumbs} />
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        {description && (
          <p className="text-sm text-muted-foreground">{description}</p>
        )}
      </div>
    </div>
  );
}
