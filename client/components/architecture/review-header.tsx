import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { BRAND } from "@/lib/brand";
import { cn } from "@/lib/utils";

export function ArchitectureReviewHeader() {
  return (
    <header className="border-b border-border/80 bg-muted/30">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="space-y-2">
            <Badge variant="secondary" className="font-normal">
              Review mode
            </Badge>
            <h1 className="font-heading text-3xl font-semibold tracking-tight sm:text-4xl">
              System Architecture
            </h1>
            <p className="max-w-2xl text-sm text-muted-foreground sm:text-base">
              Database and data architecture of {BRAND.name} —{" "}
              {BRAND.tagline.toLowerCase()}.
            </p>
            <p className="text-sm font-medium text-foreground/80">
              Database · Multi-tenancy · Data flow · Security
            </p>
          </div>
          <Link href="/" className={cn(buttonVariants({ variant: "outline" }), "shrink-0")}>
            Back to home
          </Link>
        </div>
      </div>
    </header>
  );
}
