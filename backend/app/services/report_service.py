"""Academic report HTML/PDF rendering."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.api.v1.analytics_filters import AnalyticsFilterParams
from app.schemas.report import ReportContext
from app.services.report_charts import (
    at_risk_charts_html,
    institutional_charts_html,
    report_analytics_charts_html,
)
from app.services.report_data_service import build_report_context

_CHART_STYLES = """
.charts { margin-top: 2rem; }
.chart-grid { display: grid; gap: 1rem; }
.chart-card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 1rem; background: #fff; }
.chart-card-wide { grid-column: 1 / -1; }
.chart-svg { width: 100%; max-width: 720px; height: auto; display: block; }
.chart-svg-donut { max-width: 260px; margin: 0 auto; }
.chart-title { font-size: 13px; font-weight: 600; fill: #111827; }
.chart-subtitle { font-size: 12px; fill: #6b7280; }
.chart-label { font-size: 11px; fill: #374151; }
.chart-value { font-size: 11px; fill: #111827; font-weight: 600; }
.chart-empty { color: #6b7280; font-size: 13px; margin: 0; }
.chart-donut-wrap { display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; }
.chart-legend { display: grid; gap: 0.5rem; font-size: 12px; color: #374151; }
.badge-low { background:#dcfce7;color:#166534;padding:2px 8px;border-radius:999px;font-size:12px; }
.badge-medium { background:#fef9c3;color:#854d0e;padding:2px 8px;border-radius:999px;font-size:12px; }
.badge-high { background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:999px;font-size:12px; }
"""


def _html_shell(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 2rem; color: #111; }}
h1 {{ margin-bottom: 0.25rem; }}
h2 {{ margin-top: 1.5rem; }}
p.meta {{ color: #555; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
ul.findings li {{ margin-bottom: 0.5rem; }}
{_CHART_STYLES}
</style></head><body>{body}</body></html>"""


def _risk_badge(level: str) -> str:
    normalized = (level or "").upper()
    css = {"LOW": "badge-low", "MEDIUM": "badge-medium", "HIGH": "badge-high"}.get(normalized, "")
    return f'<span class="{css}">{normalized}</span>'


def _filter_meta(context: ReportContext) -> str:
    f = context.header.filters
    return (
        f"<p class='meta'><strong>Academic Year:</strong> {f.academic_year}<br>"
        f"<strong>Semester:</strong> {f.semester}<br>"
        f"<strong>Department:</strong> {f.department}<br>"
        f"<strong>Program:</strong> {f.program}<br>"
        f"<strong>Course:</strong> {f.course}<br>"
        f"<strong>Risk Level:</strong> {f.risk_level}<br>"
        f"<strong>Generated:</strong> {context.header.generated_at.strftime('%Y-%m-%d %H:%M UTC')}</p>"
    )


def render_institutional_report_html(context: ReportContext, include_charts: bool = False) -> str:
    overview = context.kpis.overview
    dept_rows = "".join(
        f"<tr><td>{d.department_name}</td><td>{d.average_cgpa}</td>"
        f"<td>{d.pass_percentage}%</td><td>{d.student_count}</td></tr>"
        for d in context.department_analytics
    )
    course_rows = "".join(
        f"<tr><td>{c.course_name}</td><td>{c.average_marks}</td><td>{c.pass_percentage}%</td></tr>"
        for c in context.course_performance
    )
    at_risk_rows = "".join(
        f"<tr><td>{s.roll_number}</td><td>{s.student_name}</td><td>{s.department_name or '—'}</td>"
        f"<td>{s.semester or '—'}</td><td>{s.cgpa if s.cgpa is not None else '—'}</td>"
        f"<td>{s.attendance_percentage if s.attendance_percentage is not None else '—'}</td>"
        f"<td>{s.backlog_count if s.backlog_count is not None else '—'}</td>"
        f"<td>{s.risk_score:.1f}</td><td>{_risk_badge(s.risk_level)}</td>"
        f"<td>{s.performance_trend or '—'}</td></tr>"
        for s in context.at_risk_students
    )
    findings_html = "".join(f"<li>{finding}</li>" for finding in context.findings)
    charts_html = ""
    if include_charts:
        charts_html = institutional_charts_html(
            context.department_analytics,
            context.risk_distribution,
            context.department_risk_stacks,
        )
        charts_html += report_analytics_charts_html(context)

    body = f"""
    <h1>{context.header.institution_name}</h1>
    <h2>{context.header.title}</h2>
    {_filter_meta(context)}
    <h2>Summary KPIs</h2>
    <table>
      <tr><th>Total Students</th><td>{overview.total_students}</td></tr>
      <tr><th>Average CGPA</th><td>{overview.average_cgpa}</td></tr>
      <tr><th>Average SGPA</th><td>{overview.average_sgpa}</td></tr>
      <tr><th>Pass Percentage</th><td>{overview.pass_percentage}%</td></tr>
      <tr><th>Fail Percentage</th><td>{context.kpis.fail_percentage}%</td></tr>
      <tr><th>At-Risk Percentage</th><td>{overview.at_risk_percentage}%</td></tr>
      <tr><th>High-Risk Students</th><td>{overview.high_risk_count}</td></tr>
      <tr><th>Average Attendance</th><td>{context.kpis.average_attendance}%</td></tr>
      <tr><th>Avg Predicted Marks</th><td>{context.kpis.average_predicted_marks}</td></tr>
      <tr><th>Avg Pass Probability</th><td>{context.kpis.average_pass_probability}%</td></tr>
      <tr><th>Avg Risk Score</th><td>{context.kpis.average_risk_score}</td></tr>
    </table>
    <h2>Key Findings</h2>
    <ul class="findings">{findings_html or '<li>No notable findings for this scope.</li>'}</ul>
    <h2>Department Summary</h2>
    <table>
      <tr><th>Department</th><th>Avg CGPA</th><th>Pass %</th><th>Students</th></tr>
      {dept_rows or '<tr><td colspan="4">No department data.</td></tr>'}
    </table>
    <h2>Course Performance</h2>
    <table>
      <tr><th>Course</th><th>Avg Marks</th><th>Pass %</th></tr>
      {course_rows or '<tr><td colspan="3">No course data.</td></tr>'}
    </table>
    {charts_html}
    <h2>At-Risk Students</h2>
    <table>
      <tr><th>Roll No</th><th>Name</th><th>Department</th><th>Semester</th><th>CGPA</th>
      <th>Attendance</th><th>Backlogs</th><th>Risk Score</th><th>Risk</th><th>Trend</th></tr>
      {at_risk_rows or '<tr><td colspan="10">No students in scope.</td></tr>'}
    </table>
    """
    return _html_shell(context.header.title, body)


def generate_institutional_report(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams | None = None,
    include_charts: bool = False,
    scope_ids: list[uuid.UUID] | None = None,
) -> str:
    context = build_report_context(db, institution_id, filters, scope_ids)
    return render_institutional_report_html(context, include_charts)


def generate_at_risk_report(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams | None = None,
    include_charts: bool = False,
    scope_ids: list[uuid.UUID] | None = None,
) -> str:
    context = build_report_context(db, institution_id, filters, scope_ids)
    at_risk_rows = "".join(
        f"<tr><td>{s.roll_number}</td><td>{s.student_name}</td>"
        f"<td>{_risk_badge(s.risk_level)}</td><td>{s.risk_score:.1f}</td></tr>"
        for s in context.at_risk_students
    )
    charts_html = at_risk_charts_html(context.risk_distribution, context.department_risk_stacks) if include_charts else ""
    body = f"""
    <h1>At-Risk Students Report</h1>
    {_filter_meta(context)}
    {charts_html}
    <h2>At-Risk Roster</h2>
    <table>
      <tr><th>Roll Number</th><th>Name</th><th>Risk Level</th><th>Risk Score</th></tr>
      {at_risk_rows or '<tr><td colspan="4">No at-risk students found.</td></tr>'}
    </table>
    """
    return _html_shell("At-Risk Students Report", body)


def generate_student_prediction_report(
    db: Session, institution_id: uuid.UUID, student_id: uuid.UUID
) -> str:
    from app.models.prediction import PredictionResult
    from app.models.student import Student

    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.institution_id == institution_id)
        .first()
    )
    if not student:
        raise ValueError("Student not found")
    prediction = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.student_id == student_id,
            PredictionResult.institution_id == institution_id,
        )
        .order_by(PredictionResult.created_at.desc())
        .first()
    )
    if not prediction:
        raise ValueError("No prediction found for student")

    factors = prediction.risk_factors or []
    if isinstance(factors, dict):
        factors = list(factors.values()) if factors else list(factors.keys())
    recs = prediction.recommendations or []
    if isinstance(recs, dict):
        recs = list(recs.values()) if recs else list(recs.keys())

    body = f"""
    <h1>Student Prediction Report</h1>
    <p class="meta">{student.name} ({student.roll_number})</p>
    <table>
      <tr><th>Predicted End Marks</th><td>{prediction.predicted_end_marks}</td></tr>
      <tr><th>Pass/Fail</th><td>{prediction.pass_fail_prediction}</td></tr>
      <tr><th>Pass Probability</th><td>{prediction.pass_probability}</td></tr>
      <tr><th>Risk Level</th><td>{_risk_badge(prediction.risk_level or '')}</td></tr>
      <tr><th>Risk Score</th><td>{prediction.risk_score}</td></tr>
    </table>
    <h2>Risk Factors</h2>
    <ul>{''.join(f'<li>{f}</li>' for f in factors) or '<li>None identified</li>'}</ul>
    <h2>Recommendations</h2>
    <ul>{''.join(f'<li>{r}</li>' for r in recs) or '<li>None</li>'}</ul>
    """
    return _html_shell("Student Prediction Report", body)
