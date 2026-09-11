"""Tenant isolation tests."""

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"


def _login(client, email: str, password: str, role: str = "institution_admin"):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": email, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


class TestTenantIsolation:
    def test_institution1_admin_cannot_access_institution2_student(self, client):
        """Admin from institution 1 must not read institution 2 student by ID."""
        login1 = _login(client, "admin@demo.com", "admin123")
        assert login1.status_code == 200

        login2 = _login(client, "admin@riverside.edu", "admin123")
        assert login2.status_code == 200

        students2 = client.get(f"{API}/students")
        assert students2.status_code == 200
        inst2_student_id = students2.json()["data"][0]["id"]

        _login(client, "admin@demo.com", "admin123")
        response = client.get(f"{API}/students/{inst2_student_id}")
        assert response.status_code == 404

    def test_institution1_admin_list_excludes_institution2_students(self, client):
        from tests.seed_fixtures import list_students

        _login(client, "admin@demo.com", "admin123")
        roll_numbers = [s["roll_number"] for s in list_students(client)]
        assert "20231ECE9999" not in roll_numbers
        assert "20231CSE0260" in roll_numbers
