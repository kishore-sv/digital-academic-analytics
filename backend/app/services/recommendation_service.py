"""Generate academic improvement recommendations from detected risk factors."""

from __future__ import annotations

from typing import Any

_RECOMMENDATIONS: dict[str, str] = {
    "low_attendance": "Improve class attendance to reduce academic risk.",
    "low_cgpa": "Focus on strengthening overall academic performance to raise your CGPA.",
    "backlogs": "Prioritize clearing pending backlogs to improve academic standing.",
    "failed_courses": "Work with faculty to address currently failing courses.",
    "low_performance_courses": "Review study strategies for courses with low performance.",
    "low_study_hours": "Increase consistent weekly study time.",
    "low_assignment_completion": "Complete pending assignments consistently.",
    "declining_performance": "Review recent performance trends with your faculty advisor.",
    "low_ca": "Focus on internal assessments and continuous preparation.",
    "low_mid": "Strengthen preparation before major assessments.",
}


def detect_risk_factors(features: dict[str, Any]) -> list[str]:
    """Identify human-readable risk factors from academic features."""
    factors: list[str] = []

    attendance = features.get("attendance_percentage")
    if attendance is not None and float(attendance) < 75:
        factors.append("Low attendance")

    cgpa = features.get("previous_cgpa")
    if cgpa is not None and float(cgpa) < 6.0:
        factors.append("Previous CGPA below expected level")

    backlogs = features.get("backlog_count")
    if backlogs is not None and int(backlogs) >= 2:
        factors.append("Multiple backlogs")
    elif backlogs is not None and int(backlogs) == 1:
        factors.append("Active backlog")

    failed = features.get("current_failed_courses")
    if failed is not None and int(failed) >= 1:
        factors.append("Currently failing courses")

    low_perf = features.get("low_performance_course_count")
    if low_perf is not None and int(low_perf) >= 2:
        factors.append("Multiple low-performance courses")

    study = features.get("study_hours_per_week")
    if study is not None and float(study) < 10:
        factors.append("Low weekly study hours")

    assignment = features.get("assignment_completion_percentage") or features.get(
        "assignment_completion_pct"
    )
    if assignment is not None and float(assignment) < 70:
        factors.append("Low assignment completion")

    trend = features.get("performance_trend")
    if trend and str(trend).upper() == "DECLINING":
        factors.append("Declining performance")

    ca = features.get("CA_mark")
    if ca is not None and float(ca) < 50:
        factors.append("Low internal assessment marks")

    mid = features.get("MID_mark")
    if mid is not None and float(mid) < 50:
        factors.append("Low mid-term marks")

    return factors


def generate_recommendations(features: dict[str, Any]) -> list[str]:
    """Generate actionable recommendations based on detected factors."""
    recs: list[str] = []

    attendance = features.get("attendance_percentage")
    if attendance is not None and float(attendance) < 75:
        recs.append(_RECOMMENDATIONS["low_attendance"])

    cgpa = features.get("previous_cgpa")
    if cgpa is not None and float(cgpa) < 6.0:
        recs.append(_RECOMMENDATIONS["low_cgpa"])

    backlogs = features.get("backlog_count")
    if backlogs is not None and int(backlogs) >= 1:
        recs.append(_RECOMMENDATIONS["backlogs"])

    failed = features.get("current_failed_courses")
    if failed is not None and int(failed) >= 1:
        recs.append(_RECOMMENDATIONS["failed_courses"])

    low_perf = features.get("low_performance_course_count")
    if low_perf is not None and int(low_perf) >= 1:
        recs.append(_RECOMMENDATIONS["low_performance_courses"])

    study = features.get("study_hours_per_week")
    if study is not None and float(study) < 15:
        recs.append(_RECOMMENDATIONS["low_study_hours"])

    assignment = features.get("assignment_completion_percentage") or features.get(
        "assignment_completion_pct"
    )
    if assignment is not None and float(assignment) < 70:
        recs.append(_RECOMMENDATIONS["low_assignment_completion"])

    trend = features.get("performance_trend")
    if trend and str(trend).upper() == "DECLINING":
        recs.append(_RECOMMENDATIONS["declining_performance"])

    ca = features.get("CA_mark")
    if ca is not None and float(ca) < 50:
        recs.append(_RECOMMENDATIONS["low_ca"])

    mid = features.get("MID_mark")
    if mid is not None and float(mid) < 50:
        recs.append(_RECOMMENDATIONS["low_mid"])

    return recs
