"""JWT refresh token tests."""

import uuid
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"


class TestAuthRefresh:
    def test_refresh_returns_new_access_cookie(self, client):
        email = f"refresh-{uuid.uuid4().hex[:8]}@example.com"
        signup = client.post(
            f"{API}/auth/signup",
            json={
                "name": "Refresh Test",
                "email": email,
                "password": "testpass123",
                "institution_name": "Refresh University",
            },
        )
        assert signup.status_code == 200
        assert "refresh_token" in signup.cookies

        client.cookies.clear()
        client.cookies.set("refresh_token", signup.cookies["refresh_token"])

        response = client.post(f"{API}/auth/refresh")
        assert response.status_code == 200
        assert "access_token" in response.cookies

    def test_refresh_without_token_returns_401(self):
        from app.main import app
        from fastapi.testclient import TestClient

        with TestClient(app) as fresh_client:
            response = fresh_client.post(f"{API}/auth/refresh")
            assert response.status_code == 401

    def test_refresh_with_invalid_token_returns_401(self):
        from app.main import app
        from fastapi.testclient import TestClient

        with TestClient(app) as fresh_client:
            fresh_client.cookies.set("refresh_token", "invalid.token.here")
            response = fresh_client.post(f"{API}/auth/refresh")
            assert response.status_code == 401
