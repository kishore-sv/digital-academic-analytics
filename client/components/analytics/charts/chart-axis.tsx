/** Shared Recharts axis props for readable category labels. */

/** Diagonal labels (~45°) — readable and fits long names without clipping. */
export const verticalCategoryXAxisProps = {
  tickLine: false,
  // axisLine: false,
  angle: -45,
  textAnchor: "end" as const,
  height: 56,
  interval: 0,
  tick: { fontSize: 10 },
};

export const categoryBarChartMargin = {
  left: 8,
  right: 16,
  bottom: 4,
};
