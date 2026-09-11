"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import {
  categoryBarChartMargin,
  verticalCategoryXAxisProps,
} from "@/components/analytics/charts/chart-axis";
import type { DepartmentAnalytics } from "@/types/analytics";

const chartConfig = {
  average_cgpa: { label: "Avg CGPA", color: "hsl(221 83% 53%)" },
} satisfies ChartConfig;

export function DepartmentPerformanceChart({
  departments,
}: {
  departments: DepartmentAnalytics[];
}) {
  if (departments.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">No department data available.</p>
    );
  }

  const chartData = departments.map((d) => ({
    name: d.department_name,
    average_cgpa: d.average_cgpa,
  }));

  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <BarChart data={chartData} margin={categoryBarChartMargin}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="name" {...verticalCategoryXAxisProps} />
        <YAxis domain={[0, 10]} tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Bar dataKey="average_cgpa" fill="var(--color-average_cgpa)" radius={4} />
      </BarChart>
    </ChartContainer>
  );
}
