"use client";

import { CartesianGrid, Legend, Line, LineChart, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { PerformanceTrendPoint } from "@/types/analytics";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  sgpa: { label: "SGPA", color: CHART_COLORS.primary },
  cgpa: { label: "CGPA", color: CHART_COLORS.secondary },
} satisfies ChartConfig;

function formatTrendValue(value: unknown) {
  if (value == null || value === "") {
    return null;
  }
  const numeric = typeof value === "number" ? value : Number(value);
  if (Number.isNaN(numeric)) {
    return String(value);
  }
  return numeric.toFixed(2);
}

export function PerformanceTrendChart({ data }: { data: PerformanceTrendPoint[] }) {
  const chartData = data.map((point) => ({
    semester: point.semester,
    sgpa: point.average_sgpa ?? undefined,
    cgpa: point.average_cgpa ?? undefined,
  }));

  const hasValues = chartData.some(
    (point) => point.sgpa != null || point.cgpa != null,
  );

  if (!hasValues) {
    return (
      <p className="text-sm text-muted-foreground">
        No CGPA/SGPA progression data available yet.
      </p>
    );
  }

  return (
    <ChartContainer config={chartConfig} className="aspect-[16/9] w-full">
      <LineChart data={chartData} margin={{ left: 8, right: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="semester" tickLine={false} axisLine={false} />
        <YAxis domain={[0, 10]} tickLine={false} axisLine={false} />
        <ChartTooltip
          content={
            <ChartTooltipContent
              labelKey="semester"
              formatter={(value, _name, item) => {
                const dataKey = String(item.dataKey ?? "");
                const payloadValue =
                  value ??
                  (dataKey
                    ? (item.payload as Record<string, unknown> | undefined)?.[
                        dataKey
                      ]
                    : undefined);
                const formatted = formatTrendValue(payloadValue);
                if (formatted == null) {
                  return null;
                }
                const label =
                  chartConfig[dataKey as keyof typeof chartConfig]?.label ??
                  dataKey;
                return `${label}: ${formatted}`;
              }}
            />
          }
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="sgpa"
          name="SGPA"
          stroke="var(--color-sgpa)"
          strokeWidth={2}
          connectNulls={false}
          dot={{ r: 3 }}
        />
        <Line
          type="monotone"
          dataKey="cgpa"
          name="CGPA"
          stroke="var(--color-cgpa)"
          strokeWidth={2}
          connectNulls={false}
          dot={{ r: 3 }}
        />
      </LineChart>
    </ChartContainer>
  );
}
