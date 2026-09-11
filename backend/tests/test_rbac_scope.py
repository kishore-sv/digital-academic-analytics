"""RBAC scope tests for faculty, parent, student, and admin."""

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"

PREDICTION_BODY = {
    "CA_mark": 75,
    "MID_mark": 70,
    "attendance_percentage": 85,
    "study_hours_per_week": 15,
    "assignment_completion_pct": 90,
    "previous_sgpa": 7.5,
    "previous_cgpa": 7.2,
    "backlog_count": 0,
    "course_credits": 3,
    "course_type": "THEORY",
    "branch": "CSE",
    "semester": 5,
}


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


class TestRBACScope:
    def test_faculty_can_access_assigned_student(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        students = client.get(f"{API}/students?limit=100")
        assert students.status_code == 200
        assert len(students.json()["data"]) >= 1
        student_id = students.json()["data"][0]["id"]
        detail = client.get(f"{API}/students/{student_id}")
        assert detail.status_code == 200

    def test_faculty_cannot_access_institution2_student(self, client):
        _login(client, "admin@riverside.edu", "admin123", "institution_admin")
        inst2_student_id = client.get(f"{API}/students").json()["data"][0]["id"]

        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/students/{inst2_student_id}")
        assert response.status_code == 404

    def test_parent_can_access_linked_child(self, client):
        _login(client, "parent@demo.com", "parent123", "parent")
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        student_id = next(
            s["id"]
            for s in client.get(f"{API}/students?limit=100").json()["data"]
            if s["roll_number"] == "20231CSE0260"
        )

        _login(client, "parent@demo.com", "parent123", "parent")
        response = client.get(f"{API}/students/{student_id}")
        assert response.status_code == 200

    def test_parent_cannot_access_unrelated_student(self, client):
        _login(client, "admin@riverside.edu", "admin123", "institution_admin")
        unrelated_id = client.get(f"{API}/students").json()["data"][0]["id"]

        _login(client, "parent@demo.com", "parent123", "parent")
        response = client.get(f"{API}/students/{unrelated_id}")
        assert response.status_code == 404

    def test_student_can_access_self(self, client):
        _login(client, "20231CSE0260", "student123", "student")
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        student_id = next(
            s["id"]
            for s in client.get(f"{API}/students?limit=100").json()["data"]
            if s["roll_number"] == "20231CSE0260"
        )

        _login(client, "20231CSE0260", "student123", "student")
        response = client.get(f"{API}/students/{student_id}")
        assert response.status_code == 200

    def test_student_cannot_list_all_students(self, client):
        _login(client, "20231CSE0260", "student123", "student")
        response = client.get(f"{API}/students")
        assert response.status_code == 403

    def test_faculty_cannot_access_admin_analytics(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/analytics/overview")
        assert response.status_code == 403

    def test_unauthenticated_predictions_return_401(self):
        from app.main import app
        from fastapi.testclient import TestClient

        with TestClient(app) as fresh_client:
            response = fresh_client.post(
                f"{API}/predictions/performance", json=PREDICTION_BODY
            )
            assert response.status_code == 401

    def test_faculty_can_use_prediction_tools(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.post(f"{API}/predictions/performance", json=PREDICTION_BODY)
        assert response.status_code == 200

    def test_student_cannot_use_prediction_tools(self, client):
        _login(client, "20231CSE0260", "student123", "student")
        response = client.post(f"{API}/predictions/performance", json=PREDICTION_BODY)
        assert response.status_code == 403
