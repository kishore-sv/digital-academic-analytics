"""ML model loading and prediction tests."""

import warnings

import pytest

warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture(scope="module", autouse=True)
def load_models():
    from app.ml.model_loader import model_loader
    if not model_loader.is_loaded:
        model_loader.load()


class TestModelLoading:
    def test_models_loaded(self):
        from app.ml.model_loader import model_loader
        assert model_loader.is_loaded
        assert model_loader.performance_model is not None
        assert model_loader.pass_fail_model is not None
        assert model_loader.risk_config is not None


class TestModel1:
    def test_performance_prediction_valid_range(self):
        from app.ml.model1 import predict_performance
        features = {
            "CA_mark": 75, "MID_mark": 70, "attendance_percentage": 85,
            "study_hours_per_week": 15, "assignment_completion_pct": 90,
            "previous_sgpa": 7.5, "previous_cgpa": 7.2, "backlog_count": 0,
            "course_credits": 3, "course_type": "THEORY", "branch": "CSE", "semester": 5,
        }
        result = predict_performance(features)
        assert 0 <= result <= 100


class TestModel2:
    def test_pass_fail_prediction(self):
        from app.ml.model2 import predict_pass_fail
        features = {
            "CA_mark": 75, "MID_mark": 70, "attendance_percentage": 85,
            "study_hours_per_week": 15, "assignment_completion_pct": 90,
            "previous_sgpa": 7.5, "previous_cgpa": 7.2, "backlog_count": 0,
            "course_credits": 3, "branch": "CSE", "semester": 5,
        }
        result = predict_pass_fail(features)
        assert result["prediction"] in ("PASS", "FAIL")
        assert 0 <= result["pass_probability"] <= 1
        assert 0 <= result["fail_probability"] <= 1


class TestModel3Risk:
    def test_risk_thresholds_low(self):
        from app.ml.risk_engine import predict_risk
        features = {
            "attendance_percentage": 90, "previous_cgpa": 8.5, "backlog_count": 0,
            "current_failed_courses": 0, "low_performance_course_count": 0,
            "study_hours_per_week": 25, "assignment_completion_percentage": 95,
            "performance_trend": "IMPROVING",
        }
        result = predict_risk(features)
        assert result["risk_score"] <= 22
        assert result["risk_level"] == "LOW"

    def test_risk_thresholds_high(self):
        from app.ml.risk_engine import predict_risk
        features = {
            "attendance_percentage": 50, "previous_cgpa": 4.5, "backlog_count": 4,
            "current_failed_courses": 3, "low_performance_course_count": 4,
            "study_hours_per_week": 5, "assignment_completion_percentage": 30,
            "performance_trend": "DECLINING",
        }
        result = predict_risk(features)
        assert result["risk_score"] > 38
        assert result["risk_level"] == "HIGH"


class TestRecommendations:
    def test_recommendations_generated(self):
        from app.services.recommendation_service import (
            detect_risk_factors,
            generate_recommendations,
        )
        features = {
            "attendance_percentage": 55, "previous_cgpa": 5.0, "backlog_count": 2,
            "current_failed_courses": 1, "study_hours_per_week": 8,
            "assignment_completion_percentage": 40, "performance_trend": "DECLINING",
            "CA_mark": 40, "MID_mark": 35,
        }
        factors = detect_risk_factors(features)
        recs = generate_recommendations(features)
        assert len(factors) > 0
        assert len(recs) > 0
