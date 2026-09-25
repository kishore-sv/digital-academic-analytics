"""ML demo UI routes."""

import warnings

import pytest
from fastapi.testclient import TestClient

warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture(scope="module")
def client():
    from app.main import app

    return TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def load_models():
    from app.ml.model_loader import model_loader

    if not model_loader.is_loaded:
        model_loader.load()


def test_ml_demo_page_loads(client: TestClient):
    response = client.get("/ml-demo")
    assert response.status_code == 200
    assert "ML Model Demonstration" in response.text
    assert "Performance Prediction" in response.text
    assert "Regression algorithm comparison" in response.text
    assert "Why we chose this approach" in response.text


def test_ml_demo_code_file_viewer(client: TestClient):
    response = client.get("/ml-demo/code-file?tab=model1&file=1")
    assert response.status_code == 200
    assert "code-viewer-page" in response.text
    assert "student_results_dataset_and_models_training.py" in response.text


def test_ml_demo_comparison_on_all_tabs(client: TestClient):
    for tab, heading in (
        ("model2", "Classification algorithm comparison"),
        ("model3", "At-risk detection approach comparison"),
    ):
        response = client.get(f"/ml-demo?tab={tab}")
        assert response.status_code == 200
        assert heading in response.text


def test_ml_demo_model1_post(client: TestClient):
    response = client.post(
        "/ml-demo/model1/predict",
        data={
            "CA_mark": 38,
            "MID_mark": 40,
            "attendance_percentage": 85,
            "study_hours_per_week": 18,
            "assignment_completion_pct": 90,
            "previous_sgpa": 7.8,
            "previous_cgpa": 7.6,
            "backlog_count": 0,
            "course_credits": 4,
            "course_type": "THEORY",
            "branch": "CSE",
            "semester": 4,
        },
    )
    assert response.status_code == 200
    assert "Predicted end-term marks" in response.text or "Prediction result" in response.text


def test_ml_demo_validation_error(client: TestClient):
    response = client.post(
        "/ml-demo/model1/predict",
        data={
            "CA_mark": 38,
            "MID_mark": 40,
            "attendance_percentage": 150,
            "study_hours_per_week": 18,
            "assignment_completion_pct": 90,
            "previous_sgpa": 7.8,
            "previous_cgpa": 7.6,
            "backlog_count": 0,
            "course_credits": 4,
            "course_type": "THEORY",
            "branch": "CSE",
            "semester": 4,
        },
    )
    assert response.status_code == 200
    assert "attendance_percentage" in response.text.lower() or "alert-error" in response.text
