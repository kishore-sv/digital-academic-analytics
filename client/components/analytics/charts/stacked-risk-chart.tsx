"use client";

import { Bar, BarChart, CartesianGrid, Legend, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { DepartmentRiskStack } from "@/types/analytics";
import { categoryBarChartMargin, verticalCategoryXAxisProps } from "./chart-axis";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  low: { label: "Low", color: CHART_COLORS.low },
  medium: { label: "Medium", color: CHART_COLORS.medium },
  high: { label: "High", color: CHART_COLORS.high },
} satisfies ChartConfig;

export function StackedRiskChart({ data }: { data: DepartmentRiskStack[] }) {
  const chartData = data.map((d) => ({
    name: d.department_name,
    low: d.low,
    medium: d.medium,
    high: d.high,
  }));
  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <BarChart data={chartData} margin={categoryBarChartMargin}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="name" {...verticalCategoryXAxisProps} />
        <YAxis tickLine={false} axisLine={false} allowDecimals={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Legend />
        <Bar dataKey="low" stackId="a" fill="var(--color-low)" />
        <Bar dataKey="medium" stackId="a" fill="var(--color-medium)" />
        <Bar dataKey="high" stackId="a" fill="var(--color-high)" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ChartContainer>
  );
}
