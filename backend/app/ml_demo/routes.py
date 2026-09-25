"""FastAPI routes for the backend-hosted ML demonstration UI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.ml.model1 import MODEL1_FEATURES, predict_performance
from app.ml.model2 import predict_pass_fail
from app.ml.risk_engine import predict_risk
from app.ml_demo.constants import (
    MODEL1_EXAMPLES,
    MODEL2_EXAMPLES,
    MODEL3_EXAMPLES,
    resolve_example_form,
)
from app.ml_demo.schemas import Model1DemoInput, Model2DemoInput, Model3DemoInput
from app.ml_demo.services import (
    get_algorithm_comparison,
    get_dataset_page,
    load_metrics,
    models_available,
    read_training_code,
    risk_contributions,
)

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(_BACKEND_ROOT / "templates"))

router = APIRouter(tags=["ml-demo"])


def _base_context(
    request: Request,
    tab: str = "model1",
    view: str | None = None,
    error: str | None = None,
    result: dict[str, Any] | None = None,
    form_values: dict[str, Any] | None = None,
    dataset_page: int = 1,
) -> dict[str, Any]:
    return {
        "request": request,
        "tab": tab,
        "view": view,
        "error": error,
        "result": result,
        "form_values": form_values or {},
        "models_loaded": models_available(),
        "metrics": {
            "model1": load_metrics("model1"),
            "model2": load_metrics("model2"),
            "model3": load_metrics("model3"),
        },
        "algorithm_comparison": get_algorithm_comparison(tab),
        "examples": {
            "model1": MODEL1_EXAMPLES,
            "model2": MODEL2_EXAMPLES,
            "model3": MODEL3_EXAMPLES,
        },
        "model1_features": MODEL1_FEATURES,
        "dataset": get_dataset_page(tab, dataset_page) if view == "dataset" else None,
        "training_code": read_training_code(tab) if view == "code" else None,
        "course_types": ["THEORY", "LAB", "PROJECT", "INTERNSHIP", "NON_CREDIT"],
        "trends": ["IMPROVING", "STABLE", "DECLINING"],
    }


@router.get("/ml-demo", response_class=HTMLResponse)
def ml_demo_index(
    request: Request,
    tab: str = "model1",
    view: str | None = None,
    page: int = 1,
    example: str | None = None,
) -> HTMLResponse:
    if tab not in ("model1", "model2", "model3"):
        tab = "model1"
    form_values = resolve_example_form(tab, example)

    ctx = _base_context(request, tab=tab, view=view, form_values=form_values, dataset_page=page)
    return templates.TemplateResponse(request, "ml_demo/index.html", ctx)


@router.get("/ml-demo/code-file", response_class=HTMLResponse)
def ml_demo_code_file(
    request: Request,
    tab: str = "model1",
    file: int = 1,
) -> HTMLResponse:
    """Standalone full-page view of a training code file (opened from the demo UI)."""
    if tab not in ("model1", "model2", "model3"):
        tab = "model1"
    training = read_training_code(tab)
    if not training.get("available"):
        raise HTTPException(status_code=404, detail="Training code not available for this model.")

    files = training["files"]
    index = file - 1
    if index < 0 or index >= len(files):
        raise HTTPException(status_code=404, detail="Code file not found.")

    entry = files[index]
    code_lang = "json" if entry["name"].endswith(".json") else "python"
    back_url = f"/ml-demo?tab={tab}&view=code"

    return templates.TemplateResponse(
        request,
        "ml_demo/code_viewer.html",
        {
            "request": request,
            "file": entry,
            "code_lang": code_lang,
            "back_url": back_url,
        },
    )


def _render(
    request: Request,
    tab: str,
    *,
    error: str | None = None,
    result: dict[str, Any] | None = None,
    form_values: dict[str, Any],
) -> HTMLResponse:
    ctx = _base_context(request, tab=tab, error=error, result=result, form_values=form_values)
    return templates.TemplateResponse(request, "ml_demo/index.html", ctx)


@router.post("/ml-demo/model1/predict", response_class=HTMLResponse)
def predict_model1(
    request: Request,
    CA_mark: float = Form(...),
    MID_mark: float = Form(...),
    attendance_percentage: float = Form(...),
    study_hours_per_week: float = Form(...),
    assignment_completion_pct: float = Form(...),
    previous_sgpa: float = Form(...),
    previous_cgpa: float = Form(...),
    backlog_count: int = Form(...),
    course_credits: int = Form(...),
    course_type: str = Form(...),
    branch: str = Form(...),
    semester: int = Form(...),
) -> HTMLResponse:
    raw = {
        "CA_mark": CA_mark,
        "MID_mark": MID_mark,
        "attendance_percentage": attendance_percentage,
        "study_hours_per_week": study_hours_per_week,
        "assignment_completion_pct": assignment_completion_pct,
        "previous_sgpa": previous_sgpa,
        "previous_cgpa": previous_cgpa,
        "backlog_count": backlog_count,
        "course_credits": course_credits,
        "course_type": course_type,
        "branch": branch.strip(),
        "semester": semester,
    }
    try:
        validated = Model1DemoInput.model_validate(raw)
    except ValidationError as exc:
        return _render(request, "model1", error=_format_validation(exc), form_values=raw)

    if not models_available():
        return _render(
            request,
            "model1",
            error="Model artifact unavailable. Ensure .pkl files exist in ML_MODELS_DIR.",
            form_values=raw,
        )

    features = validated.model_dump()
    try:
        predicted = predict_performance(features)
    except Exception as exc:  # noqa: BLE001 — demo UI must not crash
        return _render(request, "model1", error=str(exc), form_values=raw)

    return _render(
        request,
        "model1",
        result={"predicted_end_marks": predicted},
        form_values=raw,
    )


@router.post("/ml-demo/model2/predict", response_class=HTMLResponse)
def predict_model2(
    request: Request,
    CA_mark: float = Form(...),
    MID_mark: float = Form(...),
    attendance_percentage: float = Form(...),
    study_hours_per_week: float = Form(...),
    assignment_completion_pct: float = Form(...),
    previous_sgpa: float = Form(...),
    previous_cgpa: float = Form(...),
    backlog_count: int = Form(...),
    course_credits: int = Form(...),
    branch: str = Form(...),
    semester: int = Form(...),
) -> HTMLResponse:
    raw = {
        "CA_mark": CA_mark,
        "MID_mark": MID_mark,
        "attendance_percentage": attendance_percentage,
        "study_hours_per_week": study_hours_per_week,
        "assignment_completion_pct": assignment_completion_pct,
        "previous_sgpa": previous_sgpa,
        "previous_cgpa": previous_cgpa,
        "backlog_count": backlog_count,
        "course_credits": course_credits,
        "branch": branch.strip(),
        "semester": semester,
    }
    try:
        validated = Model2DemoInput.model_validate(raw)
    except ValidationError as exc:
        return _render(request, "model2", error=_format_validation(exc), form_values=raw)

    if not models_available():
        return _render(
            request,
            "model2",
            error="Model artifact unavailable. Ensure .pkl files exist in ML_MODELS_DIR.",
            form_values=raw,
        )

    try:
        outcome = predict_pass_fail(validated.model_dump())
    except Exception as exc:  # noqa: BLE001
        return _render(request, "model2", error=str(exc), form_values=raw)

    return _render(request, "model2", result=outcome, form_values=raw)


@router.post("/ml-demo/model3/predict", response_class=HTMLResponse)
def predict_model3(
    request: Request,
    attendance_percentage: float = Form(...),
    previous_cgpa: float = Form(...),
    backlog_count: int = Form(...),
    current_failed_courses: int = Form(...),
    low_performance_course_count: int = Form(...),
    study_hours_per_week: float = Form(...),
    assignment_completion_percentage: float = Form(...),
    performance_trend: str = Form(...),
) -> HTMLResponse:
    raw = {
        "attendance_percentage": attendance_percentage,
        "previous_cgpa": previous_cgpa,
        "backlog_count": backlog_count,
        "current_failed_courses": current_failed_courses,
        "low_performance_course_count": low_performance_course_count,
        "study_hours_per_week": study_hours_per_week,
        "assignment_completion_percentage": assignment_completion_percentage,
        "performance_trend": performance_trend,
    }
    try:
        validated = Model3DemoInput.model_validate(raw)
    except ValidationError as exc:
        return _render(request, "model3", error=_format_validation(exc), form_values=raw)

    if not models_available():
        return _render(
            request,
            "model3",
            error="Risk engine configuration unavailable.",
            form_values=raw,
        )

    features = validated.model_dump()
    try:
        outcome = predict_risk(features)
        contributions = risk_contributions(features)
    except Exception as exc:  # noqa: BLE001
        return _render(request, "model3", error=str(exc), form_values=raw)

    return _render(
        request,
        "model3",
        result={**outcome, "contributions": contributions},
        form_values=raw,
    )


def _format_validation(exc: ValidationError) -> str:
    parts = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err.get("loc", ()))
        parts.append(f"{loc}: {err.get('msg')}")
    return "; ".join(parts)
