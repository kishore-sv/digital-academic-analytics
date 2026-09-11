"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { DepartmentAnalytics } from "@/types/analytics";
import { categoryBarChartMargin, verticalCategoryXAxisProps } from "./chart-axis";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  pass_percentage: { label: "Pass %", color: CHART_COLORS.pass },
} satisfies ChartConfig;

export function DepartmentPassChart({
  departments,
}: {
  departments: DepartmentAnalytics[];
}) {
  const chartData = departments.map((d) => ({
    name: d.department_name,
    pass_percentage: d.pass_percentage,
  }));
  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <BarChart data={chartData} margin={categoryBarChartMargin}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="name" {...verticalCategoryXAxisProps} />
        <YAxis domain={[0, 100]} tickLine={false} axisLine={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Bar dataKey="pass_percentage" fill="var(--color-pass_percentage)" radius={4} />
      </BarChart>
    </ChartContainer>
  );
}
