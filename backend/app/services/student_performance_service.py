"""Student performance and analytics aggregation."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session, joinedload

from app.models.enrollment import Enrollment, SemesterResult
from app.models.prediction import PredictionResult
from app.models.semester import Semester
from app.models.student import Student
from app.services.result_calculation_service import grade_to_point


def build_student_performance(
    db: Session,
    student_id: uuid.UUID,
    institution_id: uuid.UUID,
) -> dict:
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.institution_id == institution_id)
        .first()
    )
    if not student:
        return {}

    semester_results = (
        db.query(SemesterResult)
        .join(Semester, SemesterResult.semester_id == Semester.id)
        .filter(
            SemesterResult.student_id == student_id,
            SemesterResult.institution_id == institution_id,
        )
        .order_by(Semester.number)
        .all()
    )

    latest_sr = semester_results[-1] if semester_results else None
    semesters_detail = []

    for sr in semester_results:
        semester = sr.semester
        enrollments = (
            db.query(Enrollment)
            .options(
                joinedload(Enrollment.course),
                joinedload(Enrollment.course_result),
            )
            .filter(
                Enrollment.student_id == student_id,
                Enrollment.semester_id == sr.semester_id,
                Enrollment.institution_id == institution_id,
            )
            .all()
        )

        courses = []
        marks_list: list[float] = []
        att_list: list[float] = []
        passed = 0
        failed = 0
        strongest = ("", 0.0)
        weakest = ("", 100.0)

        for enr in enrollments:
            cr = enr.course_result
            course = enr.course
            marks = cr.end_marks if cr else None
            grade = cr.grade if cr else None
            status = cr.status if cr else None
            gp = grade_to_point(grade or "F") if grade else None
            if marks is not None:
                marks_list.append(marks)
                if marks > strongest[1]:
                    strongest = (course.name, marks)
                if marks < weakest[1]:
                    weakest = (course.name, marks)
            if enr.attendance_percentage is not None:
                att_list.append(enr.attendance_percentage)
            if status == "PASS":
                passed += 1
            elif status == "FAIL":
                failed += 1
            courses.append({
                "course_id": str(course.id),
                "course_name": course.name,
                "course_code": course.code,
                "credits": course.credits,
                "marks": marks,
                "grade": grade,
                "grade_point": gp,
                "status": status,
                "attendance_percentage": enr.attendance_percentage,
            })

        avg_marks = round(sum(marks_list) / len(marks_list), 1) if marks_list else None
        avg_att = round(sum(att_list) / len(att_list), 1) if att_list else None

        semesters_detail.append({
            "semester_id": str(sr.semester_id),
            "semester_number": semester.number if semester else 0,
            "semester_name": semester.name if semester else "",
            "sgpa": sr.sgpa,
            "cgpa": sr.cgpa,
            "average_marks": avg_marks,
            "average_attendance": avg_att,
            "passed_courses": passed,
            "failed_courses": failed,
            "backlogs": sr.backlog_count,
            "strongest_course": strongest[0] if strongest[0] else None,
            "weakest_course": weakest[0] if weakest[0] and weakest[1] < 100 else None,
            "courses": courses,
        })

    total_credits = sum(
        c["credits"]
        for sem in semesters_detail
        for c in sem["courses"]
        if c["status"] == "PASS"
    )

    return {
        "student_id": str(student.id),
        "student_name": student.name,
        "roll_number": student.roll_number,
        "current_cgpa": latest_sr.cgpa if latest_sr else None,
        "current_sgpa": latest_sr.sgpa if latest_sr else None,
        "total_credits": total_credits,
        "backlogs": latest_sr.backlog_count if latest_sr else 0,
        "semesters": semesters_detail,
    }


def build_goal_guidance(
    db: Session,
    student_id: uuid.UUID,
    institution_id: uuid.UUID,
    target_cgpa: float | None = None,
) -> dict:
    perf = build_student_performance(db, student_id, institution_id)
    recent_sgpa = [
        s["sgpa"] for s in perf.get("semesters", []) if s.get("sgpa") is not None
    ][-3:]

    prediction = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.student_id == student_id,
            PredictionResult.institution_id == institution_id,
        )
        .order_by(PredictionResult.predicted_at.desc())
        .first()
    )
    predicted_perf = None
    if prediction and prediction.predicted_end_marks is not None:
        predicted_perf = prediction.predicted_end_marks

    current_cgpa = perf.get("current_cgpa")
    guidance: list[str] = []

    if current_cgpa and target_cgpa:
        if current_cgpa >= target_cgpa:
            guidance.append("You have already reached or exceeded your CGPA target. Consider setting a higher goal.")
        elif recent_sgpa:
            avg_recent = sum(recent_sgpa) / len(recent_sgpa)
            if avg_recent > current_cgpa:
                guidance.append(
                    "Your recent performance is improving. Maintaining an SGPA above your recent average "
                    "will help you move toward your target."
                )
            else:
                guidance.append(
                    "Your recent SGPA is below your current CGPA. Focus on improving performance in weaker subjects."
                )
            if predicted_perf and predicted_perf > 70:
                guidance.append(
                    f"Your predicted end-term performance ({predicted_perf:.0f}) suggests you are on track "
                    "if you maintain current study habits."
                )
    elif current_cgpa:
        guidance.append(f"Your current CGPA is {current_cgpa:.2f}. Set a target to track your progress.")

    required_sgpa_hint = None
    if current_cgpa and target_cgpa and target_cgpa > current_cgpa:
        # Rough estimate assuming ~20 credits per remaining semester
        gap = target_cgpa - current_cgpa
        required_sgpa_hint = round(current_cgpa + gap * 1.5, 2)
        guidance.append(
            f"To reach CGPA {target_cgpa:.2f}, aim for approximately SGPA {required_sgpa_hint:.2f} "
            "in upcoming semesters (estimate; actual requirement depends on remaining credits)."
        )

    return {
        "current_cgpa": current_cgpa,
        "target_cgpa": target_cgpa,
        "recent_sgpa": recent_sgpa,
        "predicted_performance": predicted_perf,
        "required_sgpa_hint": required_sgpa_hint,
        "guidance": guidance,
    }
