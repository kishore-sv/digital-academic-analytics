"""Tests for marks entry, result calculation, and RBAC."""

import warnings

from app.core.database import SessionLocal
from app.models.enrollment import Assessment, Enrollment
from app.services.result_calculation_service import marks_to_grade, recalculate_course_result
from tests.seed_fixtures import ADMIN_EMAIL, ADMIN_PASSWORD, API, FACULTY_EMAIL, FACULTY_PASSWORD

warnings.filterwarnings("ignore", category=UserWarning)


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


def _auth_client(client, email: str, password: str, role: str):
    _login(client, email, password, role)
    return client


class TestMarksEntry:
    def test_marks_to_grade(self):
        assert marks_to_grade(92) == "O"
        assert marks_to_grade(75) == "A"
        assert marks_to_grade(35) == "F"

    def test_bulk_marks_valid(self, client):
        _auth_client(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            assert enrollment is not None
            assessment = (
                db.query(Assessment)
                .filter(Assessment.course_id == enrollment.course_id)
                .first()
            )
            response = client.post(
                f"{API}/assessments/marks/bulk",
                json={
                    "entries": [
                        {
                            "enrollment_id": str(enrollment.id),
                            "assessment_id": str(assessment.id),
                            "marks_obtained": 18,
                        }
                    ]
                },
            )
            assert response.status_code == 200
            assert len(response.json()) == 1
        finally:
            db.close()

    def test_bulk_marks_rejects_negative(self, client):
        _auth_client(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            assessment = (
                db.query(Assessment)
                .filter(Assessment.course_id == enrollment.course_id)
                .first()
            )
            response = client.post(
                f"{API}/assessments/marks/bulk",
                json={
                    "entries": [
                        {
                            "enrollment_id": str(enrollment.id),
                            "assessment_id": str(assessment.id),
                            "marks_obtained": -5,
                        }
                    ]
                },
            )
            assert response.status_code in (400, 422)
        finally:
            db.close()

    def test_bulk_marks_rejects_above_max(self, client):
        _auth_client(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            assessment = (
                db.query(Assessment)
                .filter(Assessment.course_id == enrollment.course_id)
                .first()
            )
            response = client.post(
                f"{API}/assessments/marks/bulk",
                json={
                    "entries": [
                        {
                            "enrollment_id": str(enrollment.id),
                            "assessment_id": str(assessment.id),
                            "marks_obtained": assessment.max_marks + 10,
                        }
                    ]
                },
            )
            assert response.status_code in (400, 422)
        finally:
            db.close()

    def test_marks_grid_endpoint(self, client):
        _auth_client(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            response = client.get(
                f"{API}/assessments/marks-grid?course_id={enrollment.course_id}",
            )
            assert response.status_code == 200
            body = response.json()
            assert "assessments" in body
            assert "students" in body
        finally:
            db.close()

    def test_attendance_roster_endpoint(self, client):
        _auth_client(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            response = client.get(
                f"/api/v1/attendance/roster?course_id={enrollment.course_id}",
            )
            assert response.status_code == 200
            assert "students" in response.json()
        finally:
            db.close()

    def test_result_recalculation(self):
        db = SessionLocal()
        try:
            enrollment = db.query(Enrollment).first()
            assert enrollment is not None
            recalculate_course_result(db, enrollment)
            db.commit()
            db.refresh(enrollment)
            assert enrollment.course_result is not None
            assert enrollment.course_result.end_marks is not None
        finally:
            db.close()
