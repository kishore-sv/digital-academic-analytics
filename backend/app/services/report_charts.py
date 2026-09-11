"""SVG chart helpers for HTML/PDF reports."""

from __future__ import annotations

import html
import math
from typing import Sequence

from app.schemas.analytics import ChartBucket, DepartmentAnalytics, DepartmentRiskStack, RiskDistribution
from app.schemas.report import ReportContext

COLORS = {
    "low": "#22c55e",
    "medium": "#eab308",
    "high": "#ef4444",
    "primary": "#3b82f6",
    "grid": "#e5e7eb",
    "text": "#374151",
    "muted": "#6b7280",
}


def _esc(text: str) -> str:
    return html.escape(str(text))


def _truncate(text: str, max_len: int = 22) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def svg_horizontal_bar_chart(
    title: str,
    items: Sequence[tuple[str, float]],
    *,
    max_value: float,
    value_format: str = "{:.2f}",
) -> str:
    if not items:
        return f'<p class="chart-empty">No data for {_esc(title)}.</p>'

    row_height = 28
    label_width = 180
    bar_width = 420
    height = 40 + len(items) * row_height
    width = label_width + bar_width + 60
    rows = []

    for index, (label, value) in enumerate(items):
        y = 30 + index * row_height
        bar_len = 0 if max_value <= 0 else min(bar_width, (value / max_value) * bar_width)
        rows.append(
            f'<text x="0" y="{y + 14}" class="chart-label">{_esc(_truncate(label))}</text>'
            f'<rect x="{label_width}" y="{y + 4}" width="{bar_width}" height="18" fill="#f3f4f6" rx="4" />'
            f'<rect x="{label_width}" y="{y + 4}" width="{bar_len:.1f}" height="18" fill="{COLORS["primary"]}" rx="4" />'
            f'<text x="{label_width + bar_width + 8}" y="{y + 16}" class="chart-value">{value_format.format(value)}</text>'
        )

    return (
        f'<svg class="chart-svg" viewBox="0 0 {width} {height}" role="img" aria-label="{_esc(title)}">'
        f'<text x="0" y="16" class="chart-title">{_esc(title)}</text>'
        + "".join(rows)
        + "</svg>"
    )


def svg_donut_chart(title: str, distribution: RiskDistribution) -> str:
    segments = [
        ("Low", distribution.low, COLORS["low"]),
        ("Medium", distribution.medium, COLORS["medium"]),
        ("High", distribution.high, COLORS["high"]),
    ]
    total = sum(value for _, value, _ in segments)
    if total <= 0:
        return f'<p class="chart-empty">No data for {_esc(title)}.</p>'

    size = 260
    cx = cy = size / 2
    outer_r = 90
    inner_r = 55
    start_angle = -math.pi / 2
    paths = []
    legend = []
    angle = start_angle

    for label, value, color in segments:
        if value <= 0:
            continue
        sweep = (value / total) * 2 * math.pi
        end_angle = angle + sweep
        x1 = cx + outer_r * math.cos(angle)
        y1 = cy + outer_r * math.sin(angle)
        x2 = cx + outer_r * math.cos(end_angle)
        y2 = cy + outer_r * math.sin(end_angle)
        xi1 = cx + inner_r * math.cos(end_angle)
        yi1 = cy + inner_r * math.sin(end_angle)
        xi2 = cx + inner_r * math.cos(angle)
        yi2 = cy + inner_r * math.sin(angle)
        large_arc = 1 if sweep > math.pi else 0
        paths.append(
            f'<path d="M {x1:.2f} {y1:.2f} A {outer_r} {outer_r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} '
            f'L {xi1:.2f} {yi1:.2f} A {inner_r} {inner_r} 0 {large_arc} 0 {xi2:.2f} {yi2:.2f} Z" '
            f'fill="{color}" />'
        )
        pct = (value / total) * 100
        legend.append(
            f'<div class="chart-legend-item"><span class="chart-swatch" style="background:{color}"></span>'
            f'<span>{_esc(label)}: {value} ({pct:.1f}%)</span></div>'
        )
        angle = end_angle

    return (
        f'<div class="chart-donut-wrap">'
        f'<svg class="chart-svg chart-svg-donut" viewBox="0 0 {size} {size}" role="img" aria-label="{_esc(title)}">'
        f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" class="chart-title">{_esc(title)}</text>'
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" class="chart-subtitle">{total} students</text>'
        + "".join(paths)
        + "</svg>"
        f'<div class="chart-legend">{"".join(legend)}</div>'
        f"</div>"
    )


def svg_stacked_bar_chart(title: str, stacks: Sequence[DepartmentRiskStack]) -> str:
    if not stacks:
        return f'<p class="chart-empty">No data for {_esc(title)}.</p>'

    chart_left = 40
    chart_bottom = 180
    bar_gap = 16
    bar_width = 42
    chart_width = max(360, len(stacks) * (bar_width + bar_gap) + chart_left + 20)
    chart_height = 220
    max_total = max(stack.low + stack.medium + stack.high for stack in stacks) or 1
    plot_height = 130
    bars = []
    labels = []

    for index, stack in enumerate(stacks):
        x = chart_left + index * (bar_width + bar_gap)
        total = stack.low + stack.medium + stack.high
        y_cursor = chart_bottom
        for value, color in (
            (stack.low, COLORS["low"]),
            (stack.medium, COLORS["medium"]),
            (stack.high, COLORS["high"]),
        ):
            if value <= 0:
                continue
            height = (value / max_total) * plot_height
            y_cursor -= height
            bars.append(
                f'<rect x="{x:.1f}" y="{y_cursor:.1f}" width="{bar_width}" height="{height:.1f}" fill="{color}" />'
            )
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{chart_bottom + 16}" text-anchor="middle" class="chart-label">'
            f'{_esc(_truncate(stack.department_name, 14))}</text>'
        )

    legend = (
        f'<div class="chart-legend chart-legend-inline">'
        f'<div class="chart-legend-item"><span class="chart-swatch" style="background:{COLORS["low"]}"></span>Low</div>'
        f'<div class="chart-legend-item"><span class="chart-swatch" style="background:{COLORS["medium"]}"></span>Medium</div>'
        f'<div class="chart-legend-item"><span class="chart-swatch" style="background:{COLORS["high"]}"></span>High</div>'
        f"</div>"
    )

    return (
        legend
        + f'<svg class="chart-svg" viewBox="0 0 {chart_width} {chart_height}" role="img" aria-label="{_esc(title)}">'
        f'<text x="0" y="18" class="chart-title">{_esc(title)}</text>'
        f'<line x1="{chart_left}" y1="{chart_bottom}" x2="{chart_width - 20}" y2="{chart_bottom}" stroke="{COLORS["grid"]}" />'
        + "".join(bars)
        + "".join(labels)
        + "</svg>"
    )


def institutional_charts_html(
    departments: Sequence[DepartmentAnalytics],
    risk: RiskDistribution,
    stacks: Sequence[DepartmentRiskStack],
) -> str:
    dept_items = [(d.department_name, d.average_cgpa) for d in departments]
    return f"""
    <section class="charts">
      <h2>Charts</h2>
      <div class="chart-grid">
        <div class="chart-card">{svg_horizontal_bar_chart("Department CGPA", dept_items, max_value=10)}</div>
        <div class="chart-card">{svg_donut_chart("Risk Distribution", risk)}</div>
        <div class="chart-card chart-card-wide">{svg_stacked_bar_chart("Department Risk Breakdown", stacks)}</div>
      </div>
    </section>
    """


def at_risk_charts_html(
    risk: RiskDistribution,
    stacks: Sequence[DepartmentRiskStack],
) -> str:
    return f"""
    <section class="charts">
      <h2>Charts</h2>
      <div class="chart-grid">
        <div class="chart-card">{svg_donut_chart("Risk Distribution", risk)}</div>
        <div class="chart-card chart-card-wide">{svg_stacked_bar_chart("Department Risk Breakdown", stacks)}</div>
      </div>
    </section>
    """


def svg_vertical_bar_chart(title: str, buckets: Sequence[ChartBucket]) -> str:
    if not buckets:
        return f'<p class="chart-empty">No data for {_esc(title)}.</p>'
    max_value = max(bucket.value for bucket in buckets) or 1
    bar_width = 48
    gap = 16
    chart_left = 40
    chart_bottom = 180
    width = chart_left + len(buckets) * (bar_width + gap) + 20
    bars = []
    for index, bucket in enumerate(buckets):
        x = chart_left + index * (bar_width + gap)
        height = (bucket.value / max_value) * 120
        y = chart_bottom - height
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{height:.1f}" fill="{COLORS["primary"]}" />'
            f'<text x="{x + bar_width / 2:.1f}" y="{chart_bottom + 16}" text-anchor="middle" class="chart-label">{_esc(bucket.label)}</text>'
            f'<text x="{x + bar_width / 2:.1f}" y="{y - 6}" text-anchor="middle" class="chart-value">{int(bucket.value)}</text>'
        )
    return (
        f'<svg class="chart-svg" viewBox="0 0 {width} 210" role="img" aria-label="{_esc(title)}">'
        f'<text x="0" y="18" class="chart-title">{_esc(title)}</text>'
        + "".join(bars)
        + "</svg>"
    )


def report_analytics_charts_html(context: ReportContext) -> str:
    cgpa = svg_vertical_bar_chart("CGPA Distribution", context.cgpa_distribution)
    sgpa = svg_vertical_bar_chart("SGPA Distribution", context.sgpa_distribution)
    attendance = svg_vertical_bar_chart("Attendance Distribution", context.attendance_distribution)
    course_items = [(c.course_name, c.average_marks) for c in context.course_performance[:8]]
    course_chart = svg_horizontal_bar_chart(
        "Course Performance",
        course_items,
        max_value=max((v for _, v in course_items), default=100) or 100,
    )
    return f"""
    <section class="charts">
      <h2>Academic Analytics</h2>
      <div class="chart-grid">
        <div class="chart-card">{cgpa}</div>
        <div class="chart-card">{sgpa}</div>
        <div class="chart-card">{attendance}</div>
        <div class="chart-card chart-card-wide">{course_chart}</div>
      </div>
    </section>
    """
