"""End-to-end integration: academic data → features → ML → stored predictions."""

import warnings

import pytest
from app.core.seed_data import INSTITUTION_1_NAME, STUDENT_ROLLS
from tests.seed_fixtures import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    API,
    PRIMARY_STUDENT_ROLL,
)

warnings.filterwarnings("ignore", category=UserWarning)


def _login(client, identifier: str, password: str, role: str):
    response = client.post(
        f"{API}/auth/login",
        json={"identifier": identifier, "password": password, "role": role},
    )
    assert response.status_code == 200, response.text
    return response


@pytest.fixture(scope="module", autouse=True)
def ensure_predictions_seeded():
    """Ensure prediction results exist for seeded students."""
    from app.core.database import SessionLocal
    from app.models.institution import Institution
    from app.models.prediction import PredictionResult
    from app.models.student import Student
    from app.services.prediction_storage_service import seed_predictions_for_institution

    db = SessionLocal()
    try:
        institution = (
            db.query(Institution)
            .filter(Institution.name == INSTITUTION_1_NAME)
            .first()
        )
        if not institution:
            pytest.skip("Primary institution not seeded — run scripts/reseed.py")
        student = (
            db.query(Student)
            .filter(
                Student.institution_id == institution.id,
                Student.roll_number == PRIMARY_STUDENT_ROLL,
            )
            .first()
        )
        if not student:
            pytest.skip("Seed students missing — run scripts/reseed.py")

        existing = (
            db.query(PredictionResult)
            .filter(PredictionResult.student_id == student.id)
            .first()
        )
        if not existing:
            seed_predictions_for_institution(db, institution.id, replace_existing=False)
            db.commit()
    finally:
        db.close()


class TestIntegrationFlow:
    def test_feature_preparation_from_academic_data(self):
        from app.core.database import SessionLocal
        from app.models.institution import Institution
        from app.models.student import Student
        from app.services.feature_preparation import build_features_from_student

        db = SessionLocal()
        try:
            institution = (
                db.query(Institution)
                .filter(Institution.name == INSTITUTION_1_NAME)
                .first()
            )
            student = (
                db.query(Student)
                .filter(
                    Student.institution_id == institution.id,
                    Student.roll_number == PRIMARY_STUDENT_ROLL,
                )
                .first()
            )
            features = build_features_from_student(db, student.id, institution.id)

            assert features["CA_mark"] > 0
            assert features["MID_mark"] > 0
            assert features["attendance_percentage"] > 0
            assert features["previous_cgpa"] > 0
            assert features["branch"] == "CSE"
        finally:
            db.close()

    def test_ml_pipeline_produces_valid_predictions(self):
        from app.core.database import SessionLocal
        from app.models.institution import Institution
        from app.models.student import Student
        from app.services.feature_preparation import build_features_from_student
        from app.services.prediction_service import predict_all

        db = SessionLocal()
        try:
            institution = (
                db.query(Institution)
                .filter(Institution.name == INSTITUTION_1_NAME)
                .first()
            )
            student = (
                db.query(Student)
                .filter(
                    Student.institution_id == institution.id,
                    Student.roll_number == PRIMARY_STUDENT_ROLL,
                )
                .first()
            )
            features = build_features_from_student(db, student.id, institution.id)
            result = predict_all(features, str(student.id))

            assert 0 <= result["performance"]["predicted_end_marks"] <= 100
            assert result["pass_fail"]["prediction"] in ("PASS", "FAIL")
            assert result["risk"]["risk_level"] in ("LOW", "MEDIUM", "HIGH")
            assert isinstance(result["risk"]["risk_factors"], list)
            assert isinstance(result["risk"]["recommendations"], list)
        finally:
            db.close()

    def test_high_risk_student_has_elevated_risk(self):
        from app.core.database import SessionLocal
        from app.models.institution import Institution
        from app.models.prediction import PredictionResult
        from app.models.student import Student

        high_risk_roll = STUDENT_ROLLS[2][0]
        db = SessionLocal()
        try:
            institution = (
                db.query(Institution)
                .filter(Institution.name == INSTITUTION_1_NAME)
                .first()
            )
            student = (
                db.query(Student)
                .filter(
                    Student.institution_id == institution.id,
                    Student.roll_number == high_risk_roll,
                )
                .first()
            )
            if not student:
                pytest.skip("Seed data incomplete — run scripts/reseed.py")
            prediction = (
                db.query(PredictionResult)
                .filter(PredictionResult.student_id == student.id)
                .order_by(PredictionResult.created_at.desc())
                .first()
            )
            assert prediction is not None
            assert prediction.risk_level in ("MEDIUM", "HIGH")
            assert prediction.risk_score is not None
            assert prediction.predicted_end_marks is not None
        finally:
            db.close()

    def test_at_risk_endpoint_returns_data(self, client):
        _login(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        response = client.get(f"{API}/at-risk")
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert len(body["data"]) >= 1
        assert body["data"][0]["risk_level"] in ("MEDIUM", "HIGH")

    def test_analytics_overview_reflects_predictions(self, client):
        _login(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        response = client.get(f"{API}/analytics/overview")
        assert response.status_code == 200
        data = response.json()
        assert data["total_students"] >= 3
        assert data["at_risk_percentage"] > 0

    def test_student_prediction_api_stores_result(self, client):
        _login(client, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
        from tests.seed_fixtures import list_students

        student_id = next(
            s["id"]
            for s in list_students(client)
            if s["roll_number"] == PRIMARY_STUDENT_ROLL
        )

        response = client.post(
            f"{API}/predictions/student",
            json={"student_id": student_id},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["performance"]["predicted_end_marks"] is not None
        assert body["pass_fail"]["prediction"] in ("PASS", "FAIL")
        assert body["risk"]["risk_level"] in ("LOW", "MEDIUM", "HIGH")
