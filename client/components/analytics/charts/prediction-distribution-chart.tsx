"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { ChartBucket } from "@/types/analytics";
import { categoryBarChartMargin, verticalCategoryXAxisProps } from "./chart-axis";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  value: { label: "Count", color: CHART_COLORS.secondary },
} satisfies ChartConfig;

export function PredictionDistributionChart({ data }: { data: ChartBucket[] }) {
  const chartData = data.map((d) => ({ bucket: d.label, value: d.value }));
  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <BarChart data={chartData} margin={categoryBarChartMargin}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="bucket" {...verticalCategoryXAxisProps} />
        <YAxis tickLine={false} axisLine={false} allowDecimals={false} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Bar dataKey="value" fill="var(--color-value)" radius={4} />
      </BarChart>
    </ChartContainer>
  );
}
