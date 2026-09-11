"use client";

import { Cell, Pie, PieChart } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import { CHART_COLORS } from "@/components/analytics/charts/chart-colors";
import type { RiskDistribution } from "@/types/analytics";

const chartConfig = {
  low: { label: "Low Risk", color: CHART_COLORS.low },
  medium: { label: "Medium Risk", color: CHART_COLORS.medium },
  high: { label: "High Risk", color: CHART_COLORS.high },
} satisfies ChartConfig;

const RISK_ITEMS = [
  { key: "low" as const, label: "Low Risk", color: CHART_COLORS.low },
  { key: "medium" as const, label: "Medium Risk", color: CHART_COLORS.medium },
  { key: "high" as const, label: "High Risk", color: CHART_COLORS.high },
];

export function RiskDistributionChart({ data }: { data: RiskDistribution }) {
  const chartData = RISK_ITEMS
    .map((item) => ({
      name: item.key,
      label: item.label,
      value: data[item.key],
      fill: item.color,
    }))
    .filter((item) => item.value > 0);

  const total = chartData.reduce((sum, item) => sum + item.value, 0);

  if (chartData.length === 0 || total === 0) {
    return (
      <p className="text-sm text-muted-foreground">No risk distribution data.</p>
    );
  }

  return (
    <div className="space-y-4">
      <ChartContainer
        config={chartConfig}
        className="mx-auto aspect-square max-h-[260px] w-full min-h-[220px]"
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
        {RISK_ITEMS.map((item) => {
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
        {total} students with ML risk predictions · based on latest model run
      </p>
    </div>
  );
}
