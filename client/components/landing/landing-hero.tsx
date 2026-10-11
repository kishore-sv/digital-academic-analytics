import Link from "next/link";
import {
  IconActivity,
  IconAlertTriangle,
  IconArrowDown,
  IconBell,
  IconBuilding,
  IconChevronRight,
  IconFileText,
  IconScale,
  IconSparkles,
  IconTarget,
  IconTrendingUp,
} from "@tabler/icons-react";
import { buttonVariants } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";
import { cn } from "@/lib/utils";

const ACADEMIC_DATA = [
  "Attendance",
  "CA / Internal",
  "Mid-term",
  "End-semester",
  "Results",
  "SGPA / CGPA",
  "Backlogs",
  "Progression",
];

const FLOW_STEPS = [
  "Academic data",
  "Monitoring",
  "Analytics",
  "Prediction",
  "Risk & action",
];

const INTELLIGENCE_CHIPS = [
  "Performance",
  "Trends",
  "Institution",
  "Predictions",
  "Risk",
  "Goals",
  "Alerts",
  "Reports",
];

const PRIMARY_FEATURES = [
  {
    title: "Performance Monitoring",
    body: "Track attendance, marks, results, SGPA/CGPA and academic progression.",
    icon: IconActivity,
  },
  {
    title: "Performance & Trend Analytics",
    body: "Understand improvement, decline and long-term academic trends.",
    icon: IconTrendingUp,
  },
  {
    title: "Institutional Analytics",
    body: "Analyze departments, programs, batches, sections and courses.",
    icon: IconBuilding,
  },
  {
    title: "Predictive Analytics",
    body: "Predict academic outcomes using historical and current performance data.",
    icon: IconSparkles,
  },
  {
    title: "Risk & Early Warning",
    body: "Identify students who may need academic attention before outcomes are final.",
    icon: IconAlertTriangle,
  },
] as const;

const SECONDARY_FEATURES = [
  {
    title: "Goal & Improvement Planning",
    body: "Set academic targets, track progress and identify areas for improvement.",
    icon: IconTarget,
  },
  {
    title: "Academic Rules & Progression",
    body: "Apply university-specific promotion, attendance, passing and backlog rules.",
    icon: IconScale,
  },
  {
    title: "Alerts & Reports",
    body: "Turn insights into alerts, reports and academic decision support.",
    icon: IconBell,
    extraIcon: IconFileText,
  },
] as const;

const STAKEHOLDERS = [
  {
    role: "Admin",
    detail: "Institution-wide analytics and decision support",
  },
  {
    role: "Faculty",
    detail: "Student and course-level monitoring",
  },
  {
    role: "Students",
    detail: "Performance, goals and improvement tracking",
  },
  {
    role: "Parents",
    detail: "Progress, attendance and academic alerts",
  },
] as const;

const SCOPE_CHAIN = [
  "Students",
  "Courses",
  "Sections",
  "Batches",
  "Programs",
  "Departments",
  "Institution",
];

export function LandingHero() {
  return (
    <section className="border-b border-border/80 bg-background">
      <div className="mx-auto max-w-6xl px-5 pb-10 pt-10 sm:px-8 sm:pb-12 sm:pt-14">
        <div className="grid gap-10 lg:grid-cols-[1fr_minmax(280px,340px)] lg:items-start lg:gap-12">
          <div>
            <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
              University academic intelligence
            </p>
            <h1 className="mt-3 max-w-2xl font-heading text-3xl font-semibold tracking-tight text-foreground sm:text-4xl sm:leading-[1.12] lg:text-[2.65rem]">
              Turn university academic data into actionable intelligence
            </h1>
            <p className="mt-4 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
              ScholarPulse helps universities monitor student performance,
              understand academic trends, predict outcomes, identify students at
              risk, and make data-driven academic decisions.
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              {ACADEMIC_DATA.map((label) => (
                <span
                  key={label}
                  className="rounded-full border border-border/70 bg-muted/40 px-2.5 py-0.5 text-xs text-muted-foreground"
                >
                  {label}
                </span>
              ))}
            </div>

            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Link
                href={ROUTES.auth.signup}
                className={buttonVariants({ size: "lg" })}
              >
                Register your institution
              </Link>
              <a
                href="#screens"
                className={buttonVariants({ variant: "outline", size: "lg" })}
              >
                Explore the platform
              </a>
              <Link
                href={ROUTES.auth.login}
                className="text-sm text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
              >
                Sign in
              </Link>
            </div>
          </div>

          <div
            className="rounded-xl border border-border/80 bg-muted/20 p-5 shadow-sm"
            aria-label="Academic intelligence overview"
          >
            <p className="text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Academic intelligence
            </p>
            <div className="mt-4 flex flex-col items-center gap-1">
              {FLOW_STEPS.map((step, i) => (
                <div key={step} className="flex w-full flex-col items-center">
                  <div
                    className={cn(
                      "w-full rounded-lg border border-border/70 bg-background px-3 py-2 text-center text-sm font-medium text-foreground shadow-xs",
                      i === FLOW_STEPS.length - 1 && "border-primary/30 bg-primary/5",
                    )}
                  >
                    {step}
                  </div>
                  {i < FLOW_STEPS.length - 1 && (
                    <IconArrowDown
                      className="my-0.5 size-4 text-muted-foreground/60"
                      aria-hidden
                    />
                  )}
                </div>
              ))}
            </div>
            <div className="mt-4 flex flex-wrap justify-center gap-1.5">
              {INTELLIGENCE_CHIPS.map((chip) => (
                <span
                  key={chip}
                  className="rounded-md border border-border/60 bg-background px-2 py-1 text-[11px] font-medium text-muted-foreground"
                >
                  {chip}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-10 border-t border-border/60 pt-8">
          <p className="text-sm font-medium text-foreground">
            One connected view of academic performance — from individual
            students to the entire university.
          </p>
          <div className="mt-3 flex flex-wrap items-center gap-1 text-xs text-muted-foreground sm:text-sm">
            {SCOPE_CHAIN.map((item, i) => (
              <span key={item} className="flex items-center gap-1">
                <span className="font-medium text-foreground/90">{item}</span>
                {i < SCOPE_CHAIN.length - 1 && (
                  <IconChevronRight className="size-3.5 shrink-0 opacity-50" />
                )}
              </span>
            ))}
          </div>
        </div>

        <div className="mt-8">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            What your university gets
          </h2>
          <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {PRIMARY_FEATURES.map((item) => {
              const Icon = item.icon;
              return (
                <li
                  key={item.title}
                  className="rounded-lg border border-border bg-background p-4 shadow-sm ring-1 ring-primary/5"
                >
                  <Icon
                    className="size-4 text-primary"
                    aria-hidden
                    stroke={1.75}
                  />
                  <h3 className="mt-2 text-sm font-semibold text-foreground">
                    {item.title}
                  </h3>
                  <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                    {item.body}
                  </p>
                </li>
              );
            })}
            {SECONDARY_FEATURES.map((item) => {
              const Icon = item.icon;
              const Extra =
                "extraIcon" in item ? item.extraIcon : undefined;
              return (
                <li
                  key={item.title}
                  className="rounded-lg border border-border/70 bg-muted/30 p-4 shadow-xs"
                >
                  <div className="flex items-center gap-2">
                    <Icon
                      className="size-4 text-muted-foreground"
                      aria-hidden
                      stroke={1.75}
                    />
                    {Extra && (
                      <Extra
                        className="size-3.5 text-muted-foreground/70"
                        aria-hidden
                        stroke={1.75}
                      />
                    )}
                  </div>
                  <h3 className="mt-2 text-sm font-medium text-foreground">
                    {item.title}
                  </h3>
                  <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                    {item.body}
                  </p>
                </li>
              );
            })}
          </ul>
          <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground lg:col-span-4">
            Academic rules and progression support configurable university
            policies; alerts and reports turn monitoring into action.
          </p>
        </div>

        <div className="mt-8 rounded-lg border border-border/60 bg-muted/25 px-4 py-4 sm:px-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            Built for the entire academic ecosystem
          </p>
          <ul className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {STAKEHOLDERS.map((s) => (
              <li key={s.role} className="text-sm">
                <span className="font-medium text-foreground">{s.role}</span>
                <span className="text-muted-foreground"> — {s.detail}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
