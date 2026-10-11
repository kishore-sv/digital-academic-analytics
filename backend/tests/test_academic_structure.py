"""Academic master-data structure tests."""

import uuid
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

from tests.academic_helpers import _login, new_student_payload, reference_student_placement
from tests.seed_fixtures import API, list_students

API_V1 = API


def _paginated(response):
    body = response.json()
    return body["data"]


class TestAcademicStructure:
    def test_academic_year_crud_and_single_current(self, client):
        _login(client)
        name = f"AY-{uuid.uuid4().hex[:6]}"
        create = client.post(
            f"{API_V1}/academic/years",
            json={"name": name, "is_current": True},
        )
        assert create.status_code == 201
        year_id = create.json()["id"]
        assert create.json()["is_current"] is True

        years = client.get(f"{API_V1}/academic/years").json()
        current = [y for y in years if y["is_current"]]
        assert len(current) == 1

        delete = client.delete(f"{API_V1}/academic/years/{year_id}")
        assert delete.status_code == 204

    def test_semester_create_with_year_number(self, client):
        _login(client)
        years = client.get(f"{API_V1}/academic/years").json()
        year_id = years[0]["id"]
        num = 9 + int(uuid.uuid4().hex[:2], 16) % 3
        create = client.post(
            f"{API_V1}/academic/semesters",
            json={
                "academic_year_id": year_id,
                "number": num,
                "name": f"Semester {num}",
                "year_number": 5,
            },
        )
        assert create.status_code == 201
        assert create.json()["year_number"] == 5

    def test_batch_class_section_hierarchy(self, client):
        _login(client)
        program_id = _paginated(client.get(f"{API_V1}/programs"))[0]["id"]
        batch = client.post(
            f"{API_V1}/batches",
            json={
                "program_id": program_id,
                "admission_year": 2020,
                "code": f"B{uuid.uuid4().hex[:4]}",
                "name": "Batch Test",
            },
        )
        assert batch.status_code == 201
        batch_id = batch.json()["id"]

        cg = client.post(
            f"{API_V1}/class-groups",
            json={
                "batch_id": batch_id,
                "year_number": 2,
                "code": "Y2",
                "name": "Year 2",
            },
        )
        assert cg.status_code == 201
        cg_id = cg.json()["id"]

        section = client.post(
            f"{API_V1}/sections",
            json={
                "class_group_id": cg_id,
                "code": "Z",
                "name": "Section Z",
            },
        )
        assert section.status_code == 201

    def test_student_create_with_placement(self, client):
        _login(client)
        payload = new_student_payload(client)
        create = client.post(f"{API_V1}/students", json=payload)
        assert create.status_code == 201
        body = create.json()
        assert body["semester_number"] is not None
        assert body["section_code"] is not None

    def test_student_invalid_program_department(self, client):
        _login(client)
        depts = _paginated(client.get(f"{API_V1}/departments"))
        programs = _paginated(client.get(f"{API_V1}/programs"))
        placement = reference_student_placement(client)
        wrong_dept = depts[1]["id"] if len(depts) > 1 else depts[0]["id"]
        payload = new_student_payload(client)
        payload["department_id"] = wrong_dept
        payload["program_id"] = programs[0]["id"]
        if payload["department_id"] == programs[0]["department_id"]:
            return
        response = client.post(f"{API_V1}/students", json=payload)
        assert response.status_code in (400, 422)

    def test_marks_grid_loads(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        courses = _paginated(client.get(f"{API_V1}/courses"))
        assert courses
        course_id = courses[0]["id"]
        response = client.get(
            f"{API_V1}/assessments/marks-grid",
            params={"course_id": course_id},
        )
        assert response.status_code == 200
        assert "students" in response.json()

    def test_ml_features_from_student(self, client):
        _login(client)
        student_id = list_students(client)[0]["id"]
        from app.services.feature_preparation import build_features_from_student
        from app.core.database import SessionLocal
        from app.api.v1.helpers import parse_uuid

        db = SessionLocal()
        try:
            from app.models.student import Student

            student = db.query(Student).filter(Student.id == parse_uuid(student_id, "id")).first()
            features = build_features_from_student(db, student.id, student.institution_id)
            assert "branch" in features
            assert "semester" in features
            assert isinstance(features["semester"], int)
        finally:
            db.close()
