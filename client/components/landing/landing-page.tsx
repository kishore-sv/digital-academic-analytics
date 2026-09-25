import Link from "next/link";
import { LandingShowcase } from "@/components/landing/landing-showcase";
import { buttonVariants } from "@/components/ui/button";
import { BRAND } from "@/lib/brand";
import { getBackendOrigin } from "@/lib/api";
import { ROUTES } from "@/lib/constants";
import { LANDING_SHOWCASES } from "@/lib/landing-showcases";
import { cn } from "@/lib/utils";

const CAPABILITIES = [
  {
    title: "Day-to-day academics",
    body: "Departments, courses, marks entry, and attendance in one place for admins and faculty.",
  },
  {
    title: "Institution view",
    body: "Dashboards for pass rates, trends, and department comparisons—scoped per college.",
  },
  {
    title: "Early signals",
    body: "At-risk lists and ML-backed predictions so mentors can act before results are final.",
  },
] as const;

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
        <section className="mx-auto max-w-5xl px-5 pb-16 pt-14 sm:px-8 sm:pt-20">
          <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
            {BRAND.projectId}
          </p>
          <h1 className="mt-3 max-w-xl font-heading text-4xl font-semibold tracking-tight text-foreground sm:text-5xl sm:leading-[1.1]">
            {BRAND.name}
          </h1>
          <p className="mt-5 max-w-lg text-base leading-relaxed text-muted-foreground sm:text-lg">
            {BRAND.tagline}. Built for admins, faculty, students, and parents-each
            role sees only what they need.
          </p>
          <div className="mt-9 flex flex-wrap items-center gap-3">
            <Link href={ROUTES.auth.login} className={buttonVariants({ size: "lg" })}>
              Sign in
            </Link>
            <Link
              href={ROUTES.auth.signup}
              className={buttonVariants({ variant: "outline", size: "lg" })}
            >
              Register your institution
            </Link>
          </div>
        </section>

        <section
          id="product"
          className="border-t border-border/80 bg-muted/30 py-14 sm:py-16"
        >
          <div className="mx-auto max-w-5xl px-5 sm:px-8">
            <h2 className="font-heading text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              What you get
            </h2>
            <ul className="mt-8 grid gap-6 sm:grid-cols-3">
              {CAPABILITIES.map((item) => (
                <li
                  key={item.title}
                  className="rounded-lg border border-border/60 bg-background p-5 shadow-sm"
                >
                  <h3 className="font-medium text-foreground">{item.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                    {item.body}
                  </p>
                </li>
              ))}
            </ul>
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
