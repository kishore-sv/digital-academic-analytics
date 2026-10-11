"""Helpers for academic structure API tests."""

import uuid

from tests.seed_fixtures import API, list_students


def _login(client, identifier="admin@demo.com", password="admin123", role="institution_admin"):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


def reference_student_placement(client) -> dict[str, str]:
    """Return FK ids from an existing seeded student."""
    _login(client)
    students = list_students(client)
    assert students, "Seeded students required for placement reference"
    s = students[0]
    return {
        "department_id": s["department_id"],
        "program_id": s["program_id"],
        "batch_id": s["batch_id"],
        "class_group_id": s["class_group_id"],
        "section_id": s["section_id"],
        "current_semester_id": s["current_semester_id"],
    }


def new_student_payload(client, roll_number: str | None = None) -> dict:
    placement = reference_student_placement(client)
    roll = roll_number or f"TST{uuid.uuid4().hex[:8].upper()}"
    return {
        "name": "Test Student",
        "roll_number": roll,
        "password": "student123",
        **placement,
    }
