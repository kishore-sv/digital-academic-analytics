"""Phase 2 academic API tests."""

import uuid
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

API = "/api/v1"


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


def _paginated_data(response):
    body = response.json()
    assert "data" in body
    assert "meta" in body
    return body["data"]


def _seed_student_id(client):
    from tests.seed_fixtures import list_students

    students = list_students(client)
    return next(s["id"] for s in students if s["roll_number"] == "20231CSE0260")


class TestAcademicAPIs:
    def test_departments_crud(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")

        code = f"MECH-{uuid.uuid4().hex[:6].upper()}"
        create = client.post(
            f"{API}/departments",
            json={"name": "Mechanical Engineering", "code": code, "description": "ME dept"},
        )
        assert create.status_code == 201
        dept_id = create.json()["id"]

        listing = client.get(f"{API}/departments")
        assert listing.status_code == 200
        assert len(_paginated_data(listing)) >= 2

        detail = client.get(f"{API}/departments/{dept_id}")
        assert detail.status_code == 200
        assert detail.json()["code"] == code

        update = client.patch(
            f"{API}/departments/{dept_id}",
            json={"description": "Updated"},
        )
        assert update.status_code == 200
        assert update.json()["description"] == "Updated"

        delete = client.delete(f"{API}/departments/{dept_id}")
        assert delete.status_code == 204

    def test_institution_me(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        response = client.get(f"{API}/institutions/me")
        assert response.status_code == 200
        assert response.json()["name"] == "Demo University"

        patch = client.patch(
            f"{API}/institutions/me",
            json={"description": "Seeded institution"},
        )
        assert patch.status_code == 200
        assert patch.json()["description"] == "Seeded institution"

    def test_programs_and_courses(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        dept_id = _paginated_data(client.get(f"{API}/departments"))[0]["id"]

        program_code = f"BTECH-{uuid.uuid4().hex[:6].upper()}"
        program = client.post(
            f"{API}/programs",
            json={
                "department_id": dept_id,
                "name": "B.Tech ME",
                "code": program_code,
                "duration_semesters": 8,
            },
        )
        assert program.status_code == 201

        course_code = f"ME{uuid.uuid4().hex[:3].upper()}"
        course = client.post(
            f"{API}/courses",
            json={
                "department_id": dept_id,
                "name": "Thermodynamics",
                "code": course_code,
                "credits": 4,
                "course_type": "THEORY",
            },
        )
        assert course.status_code == 201
        assert course.json()["code"] == course_code

    def test_faculty_student_assignment(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        student_id = _seed_student_id(client)

        _login(client, "faculty@demo.com", "faculty123", "faculty")
        assigned_ids = [s["id"] for s in _paginated_data(client.get(f"{API}/students?limit=100"))]
        assert student_id in assigned_ids

    def test_parent_children_link(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        parent_id = _paginated_data(client.get(f"{API}/parents"))[0]["id"]
        student_id = _seed_student_id(client)

        children = client.get(f"{API}/parents/{parent_id}/children")
        assert children.status_code == 200
        assert student_id in children.json()

    def test_assessments_and_attendance_list(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")

        assessments = client.get(f"{API}/assessments")
        assert assessments.status_code == 200
        assert len(_paginated_data(assessments)) >= 1

        marks = client.get(f"{API}/assessments/marks")
        assert marks.status_code == 200
        assert len(_paginated_data(marks)) >= 1

        attendance = client.get(f"{API}/attendance")
        assert attendance.status_code == 200

    def test_results_endpoints(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")

        enrollments = client.get(f"{API}/results/enrollments")
        assert enrollments.status_code == 200
        assert len(_paginated_data(enrollments)) >= 1

        course_results = client.get(f"{API}/results/course")
        assert course_results.status_code == 200
        assert len(_paginated_data(course_results)) >= 1

        semester_results = client.get(f"{API}/results/semester")
        assert semester_results.status_code == 200
        assert len(_paginated_data(semester_results)) >= 1

    def test_users_admin_only(self, client):
        _login(client, "faculty@demo.com", "faculty123", "faculty")
        response = client.get(f"{API}/users")
        assert response.status_code == 403

        _login(client, "admin@demo.com", "admin123", "institution_admin")
        users = client.get(f"{API}/users")
        assert users.status_code == 200
        assert len(_paginated_data(users)) >= 4

    def test_tenant_isolation_on_departments(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        dept_id = _paginated_data(client.get(f"{API}/departments"))[0]["id"]

        _login(client, "admin@riverside.edu", "admin123", "institution_admin")
        response = client.get(f"{API}/departments/{dept_id}")
        assert response.status_code == 404

    def test_student_create(self, client):
        _login(client, "admin@demo.com", "admin123", "institution_admin")
        dept_id = _paginated_data(client.get(f"{API}/departments"))[0]["id"]

        roll_number = f"20231CSE{uuid.uuid4().hex[:4].upper()}"
        create = client.post(
            f"{API}/students",
            json={
                "name": "New Student",
                "roll_number": roll_number,
                "password": "student123",
                "department_id": dept_id,
                "semester": 1,
                "branch": "CSE",
            },
        )
        assert create.status_code == 201
        assert create.json()["roll_number"] == roll_number
