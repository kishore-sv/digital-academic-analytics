"""Analytics chart aggregation endpoint tests."""

import warnings

import pytest
from tests.seed_fixtures import ADMIN_EMAIL, ADMIN_PASSWORD, API

warnings.filterwarnings("ignore", category=UserWarning)


def _login_admin(client):
    return client.post(
        f"{API}/auth/login",
        json={
            "identifier": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "role": "institution_admin",
        },
    )


@pytest.fixture(scope="module")
def admin_client(client):
    resp = _login_admin(client)
    if resp.status_code != 200:
        pytest.skip("Admin login failed — run scripts/seed.py")
    return client


class TestAnalyticsCharts:
    def test_overview_with_filters(self, admin_client):
        r = admin_client.get(f"{API}/analytics/overview")
        assert r.status_code == 200
        data = r.json()
        assert "total_students" in data
        assert "average_cgpa" in data

    def test_cgpa_distribution(self, admin_client):
        r = admin_client.get(f"{API}/analytics/cgpa-distribution")
        assert r.status_code == 200
        buckets = r.json()
        assert isinstance(buckets, list)
        assert len(buckets) >= 1

    def test_performance_trends(self, admin_client):
        r = admin_client.get(f"{API}/analytics/performance-trends")
        assert r.status_code == 200
        trends = r.json()
        assert isinstance(trends, list)
        if trends:
            assert "average_cgpa" in trends[0]

    def test_pass_fail_trend(self, admin_client):
        r = admin_client.get(f"{API}/analytics/pass-fail-trend")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_prediction_analytics(self, admin_client):
        r = admin_client.get(f"{API}/analytics/predictions/performance")
        assert r.status_code == 200
        data = r.json()
        assert "distribution" in data

    def test_at_risk_summary(self, admin_client):
        r = admin_client.get(f"{API}/at-risk/summary")
        assert r.status_code == 200
        data = r.json()
        assert "risk_distribution" in data
        assert "department_stacks" in data

    def test_academic_years(self, admin_client):
        r = admin_client.get(f"{API}/academic/years")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_scoped_overview_faculty(self, client):
        login = client.post(
            f"{API}/auth/login",
            json={
                "identifier": "faculty@demo.com",
                "password": "faculty123",
                "role": "faculty",
            },
        )
        if login.status_code != 200:
            pytest.skip("Faculty login failed")
        r = client.get(f"{API}/analytics/scoped/overview")
        assert r.status_code == 200
