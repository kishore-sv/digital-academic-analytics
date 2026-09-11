"""Tests for report chart generation."""

API = "/api/v1"


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


class TestReportCharts:
    def test_institutional_report_without_charts(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        response = client.get(f"{API}/reports/institutional")
        assert response.status_code == 200
        assert "<section class=\"charts\">" not in response.text

    def test_institutional_report_with_charts(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        response = client.get(f"{API}/reports/institutional?include_charts=true")
        assert response.status_code == 200
        assert "<section class=\"charts\">" in response.text
        assert "Department CGPA" in response.text
        assert "Risk Distribution" in response.text

    def test_at_risk_report_with_charts(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/reports/at-risk?include_charts=true")
        assert response.status_code == 200
        assert "<section class=\"charts\">" in response.text
        assert "At-Risk Roster" in response.text
