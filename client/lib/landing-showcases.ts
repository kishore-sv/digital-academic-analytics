import type { ShowcaseItem } from "@/components/landing/landing-showcase";

export const LANDING_SHOWCASES: ShowcaseItem[] = [
  {
    src: "/landing/institutional-dashboard.png",
    alt: "ScholarPulse institutional dashboard with student counts, CGPA, pass rate, and risk charts",
    title: "Institutional dashboard",
    lead:
      "A single home screen for leadership: enrollment, faculty count, average CGPA and SGPA, pass percentage, and how many students sit in each risk band.",
    bullets: [
      "Risk distribution from the latest ML run, broken into low, medium, and high.",
      "Department CGPA bars to compare schools and branches side by side.",
      "Scoped to your institution—no cross-tenant data.",
    ],
  },
  {
    src: "/landing/analytics-overview.png",
    alt: "Analytics page with department CGPA and pass rate charts",
    title: "Analytics workspace",
    lead:
      "Filter by academic year, semester, and department, then switch between institutional KPIs, ML predictions, and at-risk views without leaving the page.",
    bullets: [
      "Summary tiles for students, average CGPA, pass %, and at-risk %.",
      "Department pass-rate and CGPA charts for accreditation-style reporting.",
      "Tabs for institutional metrics, predictions, and intervention lists.",
    ],
  },
  {
    src: "/landing/analytics-trends.png",
    alt: "Pass fail trend, attendance versus performance scatter, and performance trend donut",
    title: "Trends and correlations",
    lead:
      "See how outcomes move across semesters and whether attendance lines up with performance—useful when planning tutorials or mentor rounds.",
    bullets: [
      "Pass vs fail counts per semester with percentages on hover.",
      "Scatter plot of attendance % against course performance scores.",
      "Improving, stable, and declining cohorts in one glance.",
    ],
  },
  {
    src: "/landing/at-risk-summary.png",
    alt: "At-risk students summary with risk distribution and department risk stacks",
    title: "At-risk overview",
    lead:
      "Know how many students need attention before marks are final. Slice the same data by year, semester, and department.",
    bullets: [
      "Counts for low, medium, and high risk with a donut breakdown.",
      "Stacked bars per department showing where risk concentrates.",
      "Copy that references ML predictions from the latest model run.",
    ],
  },
  {
    src: "/landing/risk-factors.png",
    alt: "Horizontal bar chart of student risk factors such as low marks and attendance",
    title: "Risk factors",
    lead:
      "Understand why students were flagged—not just a score. Factors include internal marks, mid-terms, attendance, backlogs, and study hours.",
    bullets: [
      "Ranked counts so academic boards can prioritize interventions.",
      "Feeds from stored predictions and academic records.",
      "Pairs with faculty and mentor workflows on assigned students.",
    ],
  },
  {
    src: "/landing/at-risk-roster.png",
    alt: "At-risk roster table with roll numbers, risk level, attendance, and CGPA",
    title: "At-risk roster",
    lead:
      "Work the list: filter by department, semester, risk level, trend, attendance band, and CGPA, then open a student for detail.",
    bullets: [
      "Roll number, department, semester, risk badge, score, attendance, CGPA, trend.",
      "High/medium/low risk and improving vs declining labels.",
      "Export-friendly table layout for HOD review meetings.",
    ],
  },
];
