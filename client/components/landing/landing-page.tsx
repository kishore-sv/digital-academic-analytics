import Link from "next/link";
import { LandingHero } from "@/components/landing/landing-hero";
import { LandingShowcase } from "@/components/landing/landing-showcase";
import { buttonVariants } from "@/components/ui/button";
import { BRAND } from "@/lib/brand";
import { getBackendOrigin } from "@/lib/api";
import { ROUTES } from "@/lib/constants";
import { LANDING_SHOWCASES } from "@/lib/landing-showcases";
import { cn } from "@/lib/utils";

export function LandingPage() {
  const year = new Date().getFullYear();

  return (
    <div className="flex min-h-full flex-col bg-background">
      <header className="border-b border-border/80">
        <div className="mx-auto flex h-14 max-w-5xl items-center justify-between gap-4 px-5 sm:px-8">
          <Link
            href="/"
            className="font-heading text-lg font-semibold tracking-tight text-foreground"
          >
            {BRAND.name}
          </Link>
          <nav className="flex items-center gap-1 sm:gap-2">
            <a
              href="#product"
              className="hidden rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground sm:inline-block"
            >
              Product
            </a>
            <a
              href="#screens"
              className="hidden rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground sm:inline-block"
            >
              Screens
            </a>
            <a
              href={BRAND.apiDocsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="hidden rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground md:inline-block"
            >
              API docs
            </a>
            <Link
              href={ROUTES.auth.login}
              className={cn(
                buttonVariants({ variant: "ghost", size: "sm" }),
                "text-foreground",
              )}
            >
              Login
            </Link>
            <Link
              href={ROUTES.auth.signup}
              className={buttonVariants({ size: "sm" })}
            >
              Sign up
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <LandingHero />

        <section
          id="product"
          className="border-t border-border/80 bg-muted/30 py-10 sm:py-12"
        >
          <div className="mx-auto max-w-5xl px-5 text-center sm:px-8">
            <p className="text-sm text-muted-foreground sm:text-base">
              Multi-tenant by design — each institution&apos;s data stays isolated
              while admins, faculty, students, and parents use role-specific
              portals. Scroll for product screens and workflows.
            </p>
          </div>
        </section>

        <section id="screens" className="border-t border-border/80 py-16 sm:py-20">
          <div className="mx-auto max-w-6xl px-5 sm:px-8">
            <div className="max-w-2xl">
              <h2 className="font-heading text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                In the product
              </h2>
              <p className="mt-3 text-lg text-foreground sm:text-xl">
                Screens from the institution admin portal—dashboards, analytics, and
                at-risk workflows your team uses every week.
              </p>
            </div>
            <div className="mt-14">
              <LandingShowcase items={LANDING_SHOWCASES} />
            </div>
            <div className="mt-16 flex flex-wrap items-center justify-center gap-3 border-t border-border/80 pt-12">
              <p className="text-sm text-muted-foreground">
                Ready to explore with your own data?
              </p>
              <Link href={ROUTES.auth.signup} className={buttonVariants()}>
                Create an institution account
              </Link>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-border/80">
        <div className="mx-auto flex max-w-5xl flex-col gap-3 px-5 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between sm:px-8">
          <p>
            © {year} {BRAND.name}. Team SMK · {BRAND.projectId}.
          </p>
          <div className="flex flex-wrap gap-x-4 gap-y-1">
            <Link href={ROUTES.architecture} className="hover:text-foreground">
              System architecture
            </Link>
            <a
              href={`${getBackendOrigin()}/ml-demo`}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground"
            >
              ML Model Demo
            </a>
            <Link href={ROUTES.auth.login} className="hover:text-foreground">
              Login
            </Link>
            <a
              href={BRAND.apiDocsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground"
            >
              Backend API
            </a>
            <a
              href="https://github.com/kishore-sv/digital-academic-analytics"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-foreground"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
