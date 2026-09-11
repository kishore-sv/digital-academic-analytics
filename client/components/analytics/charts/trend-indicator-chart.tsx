"use client";

import { Cell, Pie, PieChart } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { PerformanceIndicators } from "@/types/analytics";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  improving: { label: "Improving", color: CHART_COLORS.improving },
  stable: { label: "Stable", color: CHART_COLORS.stable },
  declining: { label: "Declining", color: CHART_COLORS.declining },
} satisfies ChartConfig;

const TREND_ITEMS = [
  { key: "improving" as const, label: "Improving", color: CHART_COLORS.improving },
  { key: "stable" as const, label: "Stable", color: CHART_COLORS.stable },
  { key: "declining" as const, label: "Declining", color: CHART_COLORS.declining },
];

export function TrendIndicatorChart({ data }: { data: PerformanceIndicators }) {
  const chartData = TREND_ITEMS
    .map((item) => ({
      name: item.key,
      label: item.label,
      value: data[item.key],
      fill: item.color,
    }))
    .filter((d) => d.value > 0);

  const total = chartData.reduce((sum, item) => sum + item.value, 0);

  if (chartData.length === 0 || total === 0) {
    return (
      <p className="text-sm text-muted-foreground">No performance trend data.</p>
    );
  }

  return (
    <div className="space-y-4">
      <ChartContainer
        config={chartConfig}
        className="mx-auto aspect-square max-h-[260px] w-full min-h-[200px]"
      >
        <PieChart>
          <ChartTooltip
            content={
              <ChartTooltipContent
                nameKey="name"
                formatter={(value, _name, item) => {
                  const count = Number(value);
                  const pct = ((count / total) * 100).toFixed(1);
                  const label =
                    chartConfig[item.payload?.name as keyof typeof chartConfig]
                      ?.label ?? String(_name);
                  return `${label}: ${count} students (${pct}%)`;
                }}
              />
            }
          />
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            innerRadius={55}
            outerRadius={85}
            strokeWidth={2}
          >
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={entry.fill} />
            ))}
          </Pie>
        </PieChart>
      </ChartContainer>

      <div className="grid gap-2 sm:grid-cols-3">
        {TREND_ITEMS.map((item) => {
          const count = data[item.key];
          const pct = total > 0 ? ((count / total) * 100).toFixed(1) : "0.0";
          return (
            <div
              key={item.key}
              className="flex items-center gap-2 rounded-md border bg-muted/30 px-3 py-2"
            >
              <span
                className="size-3 shrink-0 rounded-sm"
                style={{ backgroundColor: item.color }}
                aria-hidden
              />
              <div className="min-w-0">
                <p className="text-xs font-medium leading-tight">{item.label}</p>
                <p className="text-sm text-muted-foreground">
                  <span className="font-semibold text-foreground">{count}</span>
                  {" · "}
                  {pct}%
                </p>
              </div>
            </div>
          );
        })}
      </div>

      <p className="text-center text-xs text-muted-foreground">
        {total} students · trend from latest semester results
      </p>
    </div>
  );
}
