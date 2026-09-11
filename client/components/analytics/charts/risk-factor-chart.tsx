"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { RiskFactorCount } from "@/types/analytics";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  count: { label: "Count", color: CHART_COLORS.high },
} satisfies ChartConfig;

export function RiskFactorChart({ data }: { data: RiskFactorCount[] }) {
  const chartData = data.map((d) => ({ factor: d.factor, count: d.count }));
  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <BarChart data={chartData} layout="vertical" margin={{ left: 80, right: 8 }}>
        <CartesianGrid horizontal={false} />
        <XAxis type="number" tickLine={false} axisLine={false} allowDecimals={false} />
        <YAxis type="category" dataKey="factor" tickLine={false} axisLine={false} width={75} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Bar dataKey="count" fill="var(--color-count)" radius={4} />
      </BarChart>
    </ChartContainer>
  );
}
