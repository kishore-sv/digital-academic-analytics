"""Data-driven key findings for reports."""

from app.schemas.report import ReportContext


def generate_key_findings(context: ReportContext) -> list[str]:
    findings: list[str] = []
    overview = context.kpis.overview
    total = overview.total_students

    if total == 0:
        return ["No students match the selected filters."]

    if overview.at_risk_percentage > 0:
        findings.append(
            f"{overview.at_risk_percentage:.1f}% of students in this scope are classified as at-risk."
        )
    if overview.high_risk_count > 0:
        findings.append(
            f"{overview.high_risk_count} student(s) are currently classified as high risk."
        )
    if overview.average_cgpa > 0 and overview.average_cgpa < 6.0:
        findings.append(
            f"Average CGPA ({overview.average_cgpa:.2f}) is below the 6.0 threshold."
        )
    if context.kpis.fail_percentage > 0:
        findings.append(
            f"Fail rate in this scope is {context.kpis.fail_percentage:.1f}%."
        )
    if context.kpis.average_attendance > 0 and context.kpis.average_attendance < 60:
        findings.append(
            f"Average attendance ({context.kpis.average_attendance:.1f}%) is below 60%."
        )

    indicators = context.performance_indicators
    if indicators.declining > indicators.improving and indicators.declining > 0:
        findings.append(
            f"{indicators.declining} student(s) show a declining performance trend."
        )

    if context.course_performance:
        lowest = min(context.course_performance, key=lambda c: c.average_marks)
        if lowest.average_marks > 0:
            findings.append(
                f"{lowest.course_name} has the lowest average marks ({lowest.average_marks:.1f})."
            )

    if context.risk_factors:
        top = context.risk_factors[0]
        if top.count > 0:
            findings.append(
                f'"{top.factor}" is the most common risk factor ({top.count} occurrence(s)).'
            )

    if context.prediction_pass_fail.predicted_fail_count > 0:
        findings.append(
            f"{context.prediction_pass_fail.predicted_fail_count} student(s) are predicted to fail."
        )

    return findings[:8]
