"""API integration tests."""

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


def _login_admin(client):
    return client.post(
        f"{API}/auth/login",
        json={
            "identifier": "admin@demo.com",
            "password": "admin123",
            "role": "institution_admin",
        },
    )


class TestHealth:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["models_loaded"] is True


class TestPredictions:
    def test_predict_performance_requires_auth(self):
        from app.main import app
        from fastapi.testclient import TestClient

        with TestClient(app) as fresh_client:
            response = fresh_client.post(
                f"{API}/predictions/performance", json=PREDICTION_BODY
            )
            assert response.status_code == 401

    def test_predict_performance(self, client):
        _login_admin(client)
        response = client.post(f"{API}/predictions/performance", json=PREDICTION_BODY)
        assert response.status_code == 200
        assert "predicted_end_marks" in response.json()

    def test_predict_pass_fail(self, client):
        _login_admin(client)
        body = {k: v for k, v in PREDICTION_BODY.items() if k != "course_type"}
        response = client.post(f"{API}/predictions/pass-fail", json=body)
        assert response.status_code == 200
        data = response.json()
        assert data["prediction"] in ("PASS", "FAIL")

    def test_predict_risk(self, client):
        _login_admin(client)
        response = client.post(
            f"{API}/predictions/risk",
            json={
                "attendance_percentage": 90,
                "previous_cgpa": 8.5,
                "backlog_count": 0,
                "current_failed_courses": 0,
                "low_performance_course_count": 0,
                "study_hours_per_week": 25,
                "assignment_completion_percentage": 95,
                "performance_trend": "IMPROVING",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_level"] in ("LOW", "MEDIUM", "HIGH")

    def test_predict_all(self, client):
        _login_admin(client)
        response = client.post(f"{API}/predictions/all", json=PREDICTION_BODY)
        assert response.status_code == 200
        data = response.json()
        assert "performance" in data
        assert "pass_fail" in data
        assert "risk" in data
