"""Shared seed credentials for integration tests."""

from app.core.seed_data import (  # noqa: F401 — re-exported for test modules
    ADMIN_2_EMAIL,
    ADMIN_2_PASSWORD,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    FACULTY_EMAIL,
    FACULTY_PASSWORD,
    INSTITUTION_1_NAME,
    INSTITUTION_2_NAME,
    PARENT_EMAIL,
    PARENT_PASSWORD,
    STUDENT_PASSWORD,
    STUDENT_ROLLS,
)

API = "/api/v1"
PRIMARY_STUDENT_ROLL = STUDENT_ROLLS[0][0]
STUDENTS_URL = f"{API}/students?limit=100"


def list_students(client):
    """Return all seeded students (paginated list, high limit)."""
    response = client.get(STUDENTS_URL)
    assert response.status_code == 200, response.text
    return response.json()["data"]
