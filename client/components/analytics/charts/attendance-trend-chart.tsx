"use client";

import { format, parseISO } from "date-fns";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import type { AttendanceTrendPoint } from "@/types/analytics";
import { CHART_COLORS } from "./chart-colors";

const chartConfig = {
  attendance: {
    label: "Average attendance",
    color: CHART_COLORS.primary,
  },
} satisfies ChartConfig;

function formatAxisDate(value: string) {
  const parsed = parseISO(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return format(parsed, "d MMM");
}

function formatTooltipDate(value: string) {
  const parsed = parseISO(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return format(parsed, "dd MMM yyyy");
}

export function AttendanceTrendChart({ data }: { data: AttendanceTrendPoint[] }) {
  const chartData = data.map((point) => ({
    date: point.date,
    label: formatTooltipDate(point.date),
    attendance: point.attendance_percentage,
  }));

  return (
    <ChartContainer config={chartConfig} className="aspect-[2.4/1] min-h-64 w-full">
      <LineChart data={chartData} margin={{ left: 8, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis
          dataKey="date"
          tickLine={false}
          axisLine={false}
          minTickGap={28}
          tickFormatter={formatAxisDate}
        />
        <YAxis
          domain={[0, 100]}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${value}%`}
          width={48}
        />
        <ChartTooltip
          content={
            <ChartTooltipContent
              labelFormatter={(_label, payload) => {
                const row = payload?.[0]?.payload as { label?: string } | undefined;
                return row?.label ?? "";
              }}
              formatter={(value) => {
                const numeric = typeof value === "number" ? value : Number(value);
                if (Number.isNaN(numeric)) return null;
                return `Average attendance: ${numeric.toFixed(1)}%`;
              }}
            />
          }
        />
        <Line
          type="monotone"
          dataKey="attendance"
          stroke="var(--color-attendance)"
          strokeWidth={2}
          dot={{ r: 3 }}
          connectNulls={false}
        />
      </LineChart>
    </ChartContainer>
  );
}
