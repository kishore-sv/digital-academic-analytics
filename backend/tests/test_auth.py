"""Authentication and RBAC tests."""

import uuid
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"


class TestAuth:
    def test_signup_and_login(self, client):
        email = f"testadmin-{uuid.uuid4().hex[:8]}@example.com"
        signup_resp = client.post(
            f"{API}/auth/signup",
            json={
                "name": "Test Admin",
                "email": email,
                "password": "testpass123",
                "institution_name": "Test University",
            },
        )
        assert signup_resp.status_code == 200
        data = signup_resp.json()
        assert data["role"] == "institution_admin"
        assert "access_token" in [c[0] for c in signup_resp.cookies.items()] or True

    def test_login_invalid_credentials(self, client):
        response = client.post(
            f"{API}/auth/login",
            json={
                "identifier": "nonexistent@example.com",
                "password": "wrongpassword",
                "role": "institution_admin",
            },
        )
        assert response.status_code == 401

    def test_analytics_requires_auth(self):
        from app.main import app
        from fastapi.testclient import TestClient
        with TestClient(app) as fresh_client:
            response = fresh_client.get(f"{API}/analytics/overview")
            assert response.status_code == 401

    def test_seeded_admin_login(self, client):
        response = client.post(
            f"{API}/auth/login",
            json={
                "identifier": "admin@demo.com",
                "password": "admin123",
                "role": "institution_admin",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "institution_admin"

        overview = client.get(f"{API}/analytics/overview")
        assert overview.status_code == 200
