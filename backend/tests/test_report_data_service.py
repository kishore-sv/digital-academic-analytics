"""Filtered report data service tests."""

API = "/api/v1"


def _login(client, email="admin@demo.com", password="admin123", role="institution_admin"):
    client.post(
        f"{API}/auth/login",
        json={"identifier": email, "password": password, "role": role},
    )


class TestReportDataService:
    def test_institutional_report_data(self, client):
        _login(client)
        response = client.get(f"{API}/reports/institutional/data")
        assert response.status_code == 200
        data = response.json()
        assert "header" in data
        assert "kpis" in data
        assert "findings" in data
        assert data["kpis"]["overview"]["total_students"] >= 0

    def test_filtered_report_data_by_department(self, client):
        _login(client)
        depts = client.get(f"{API}/departments").json()["data"]
        assert depts
        dept_id = depts[0]["id"]
        response = client.get(
            f"{API}/reports/institutional/data?department_id={dept_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["header"]["filters"]["department"] == depts[0]["name"]

    def test_institutional_pdf_with_filters(self, client):
        _login(client)
        response = client.get(
            f"{API}/reports/institutional/pdf?include_charts=true"
        )
        assert response.status_code == 200
        if response.status_code == 200:
            assert response.headers["content-type"] == "application/pdf"
            assert "attachment" in response.headers.get("content-disposition", "")

    def test_faculty_scoped_report_data(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/reports/scoped/institutional/data")
        assert response.status_code == 200
