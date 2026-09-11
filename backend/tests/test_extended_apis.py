"""Tests for goals, scoped analytics, and reports."""

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


class TestGoals:
    def test_student_goal_crud(self, client):
        _login(client, "20231CSE0260", "student123", "student")

        create_resp = client.post(
            f"{API}/goals",
            json={"goal_type": "cgpa", "target_value": 8.5},
        )
        assert create_resp.status_code == 201
        goal = create_resp.json()
        assert goal["goal_type"] == "cgpa"
        assert goal["target_value"] == 8.5
        goal_id = goal["id"]

        patch_resp = client.patch(
            f"{API}/goals/{goal_id}",
            json={"target_value": 9.0},
        )
        assert patch_resp.status_code == 200
        assert patch_resp.json()["target_value"] == 9.0

        list_resp = client.get(f"{API}/goals")
        assert list_resp.status_code == 200
        assert any(g["id"] == goal_id for g in list_resp.json())

        delete_resp = client.delete(f"{API}/goals/{goal_id}")
        assert delete_resp.status_code == 204


class TestScopedAnalytics:
    def test_faculty_scoped_overview(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/analytics/scoped/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_students" in data
        assert "average_cgpa" in data

    def test_student_scoped_overview(self, client):
        _login(client, "20231CSE0260", "student123", "student")
        response = client.get(f"{API}/analytics/scoped/overview")
        assert response.status_code == 200


class TestReports:
    def test_institutional_report_html(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        response = client.get(f"{API}/reports/institutional")
        assert response.status_code == 200
        assert "html" in response.headers.get("content-type", "").lower() or response.text.startswith("<")

    def test_at_risk_report_faculty(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/reports/at-risk")
        assert response.status_code == 200
