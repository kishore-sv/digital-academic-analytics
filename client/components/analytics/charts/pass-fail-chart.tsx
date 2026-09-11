"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { PassFailTrendPoint } from "@/types/analytics";
import { categoryBarChartMargin, verticalCategoryXAxisProps } from "./chart-axis";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  pass_count: { label: "Pass", color: CHART_COLORS.pass },
  fail_count: { label: "Fail", color: CHART_COLORS.fail },
} satisfies ChartConfig;

const LEGEND_ITEMS = [
  { key: "pass_count" as const, label: "Pass", color: CHART_COLORS.pass },
  { key: "fail_count" as const, label: "Fail", color: CHART_COLORS.fail },
];

export function PassFailChart({ data }: { data: PassFailTrendPoint[] }) {
  const totalPass = data.reduce((sum, d) => sum + d.pass_count, 0);
  const totalFail = data.reduce((sum, d) => sum + d.fail_count, 0);
  const total = totalPass + totalFail;

  return (
    <div className="space-y-4">
      <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
        <BarChart data={data} margin={categoryBarChartMargin}>
          <CartesianGrid vertical={false} />
          <XAxis dataKey="semester" {...verticalCategoryXAxisProps} />
          <YAxis tickLine={false} axisLine={false} allowDecimals={false} />
          <ChartTooltip
            content={
              <ChartTooltipContent
                formatter={(value, name) => {
                  const label =
                    chartConfig[name as keyof typeof chartConfig]?.label ?? name;
                  return [`${value} courses`, label];
                }}
              />
            }
          />
          <Bar dataKey="pass_count" name="Pass" fill={CHART_COLORS.pass} radius={4} />
          <Bar dataKey="fail_count" name="Fail" fill={CHART_COLORS.fail} radius={4} />
        </BarChart>
      </ChartContainer>

      <div className="flex flex-wrap justify-center gap-4">
        {LEGEND_ITEMS.map((item) => {
          const count = item.key === "pass_count" ? totalPass : totalFail;
          const pct = total > 0 ? ((count / total) * 100).toFixed(1) : "0.0";
          return (
            <div key={item.key} className="flex items-center gap-2 text-sm">
              <span
                className="size-3 shrink-0 rounded-sm"
                style={{ backgroundColor: item.color }}
                aria-hidden
              />
              <span>
                <span className="font-medium">{item.label}</span>
                {": "}
                <span className="text-muted-foreground">
                  {count} ({pct}%)
                </span>
              </span>
            </div>
          );
        })}
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Course outcomes per semester · {total} total pass/fail records
      </p>
    </div>
  );
}
