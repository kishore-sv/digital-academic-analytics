"use client";

import {
  CartesianGrid,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import type { AttendancePerformancePoint } from "@/types/analytics";
import { CHART_COLORS } from "./chart-colors";

function AttendanceTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: { payload: AttendancePerformancePoint }[];
}) {
  if (!active || !payload?.length) return null;
  const point = payload[0].payload;
  return (
    <div className="rounded-lg border bg-background px-3 py-2 text-xs shadow-md">
      <p>
        <span className="font-medium">Attendance:</span>{" "}
        {point.attendance_percentage.toFixed(1)}%
      </p>
      <p>
        <span className="font-medium">Performance:</span>{" "}
        {point.performance_value.toFixed(1)}
      </p>
    </div>
  );
}

export function AttendancePerformanceChart({
  data,
}: {
  data: AttendancePerformancePoint[];
}) {
  if (data.length === 0) return null;

  const avgAttendance =
    data.reduce((s, d) => s + d.attendance_percentage, 0) / data.length;
  const avgPerformance =
    data.reduce((s, d) => s + d.performance_value, 0) / data.length;

  return (
    <div className="space-y-4">
      <ScatterChart
        width={500}
        height={300}
        className="mx-auto w-full max-w-full"
        margin={{ top: 8, right: 16, bottom: 32, left: 16 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          type="number"
          dataKey="attendance_percentage"
          domain={[0, 100]}
          tickLine={false}
          axisLine={false}
          label={{
            value: "Attendance %",
            position: "insideBottom",
            offset: -20,
            style: { fontSize: 12, fill: "hsl(215 16% 47%)" },
          }}
        />
        <YAxis
          type="number"
          dataKey="performance_value"
          tickLine={false}
          axisLine={false}
          label={{
            value: "Performance Score",
            angle: -90,
            position: "insideLeft",
            style: { fontSize: 12, fill: "hsl(215 16% 47%)" },
          }}
        />
        <ZAxis range={[40, 40]} />
        <Tooltip content={<AttendanceTooltip />} cursor={{ strokeDasharray: "3 3" }} />
        <Scatter data={data} fill={CHART_COLORS.primary} name="Enrollment" />
      </ScatterChart>

      <div className="flex flex-wrap justify-center gap-4 text-sm">
        <div className="flex items-center gap-2">
          <span
            className="size-3 rounded-full"
            style={{ backgroundColor: CHART_COLORS.primary }}
            aria-hidden
          />
          <span>
            <span className="font-medium">Enrollment</span>
            <span className="text-muted-foreground"> · {data.length} data points</span>
          </span>
        </div>
        <span className="text-muted-foreground">
          Avg attendance: <span className="font-medium text-foreground">{avgAttendance.toFixed(1)}%</span>
        </span>
        <span className="text-muted-foreground">
          Avg performance: <span className="font-medium text-foreground">{avgPerformance.toFixed(1)}</span>
        </span>
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Each dot is one course enrollment · higher attendance generally aligns with better scores
      </p>
    </div>
  );
}
