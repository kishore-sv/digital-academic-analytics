"""Seed Demo University. Prefer scripts/reseed.py so the schema is recreated first."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.core.seed_data import (
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
    SAMPLE_FACULTY_EMPLOYEE_ID,
    STUDENT_2_ROLL,
    STUDENT_PASSWORD,
    STUDENT_ROLLS,
)
from app.core.seed_large_dataset import FULL_SPEC, seed_demo_university
from app.core.seed_validate import validate_large_dataset
from app.models.institution import Institution
from app.services.prediction_storage_service import seed_predictions_for_institution


def seed_predictions(db) -> int:
    from app.ml.model_loader import model_loader

    if not model_loader.is_loaded:
        model_loader.load()
    total = 0
    for institution in db.query(Institution).all():
        print(f"  predictions for {institution.name}...")
        total += seed_predictions_for_institution(
            db, institution.id, replace_existing=True
        )
    return total


def seed(mode: str = "large") -> None:
    """Load development data. Refuses to run when any institution already exists."""
    db = SessionLocal()
    try:
        if db.query(Institution).first():
            print("Database already has data.")
            print("Run `uv run python scripts/reseed.py` to drop and recreate it.")
            return

        if mode == "minimal":
            from scripts.seed_minimal import seed_minimal

            print("Seeding minimal dataset (pytest / tenant slice)...")
            seed_minimal(db)
            db.commit()
        else:
            print("Seeding full Demo University dataset (2,400 students)...")
            institution = seed_demo_university(db, FULL_SPEC)
            db.commit()
            validate_large_dataset(db, institution.id)

        count = seed_predictions(db)
        db.commit()
        _print_credentials(count, mode)
    finally:
        db.close()


def _print_credentials(prediction_count: int, mode: str) -> None:
    print("Seed complete.")
    print(f"Mode: {mode}")
    print(f"Institution 1 ({INSTITUTION_1_NAME}):")
    print(f"  Admin:   {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"  Faculty: {FACULTY_EMAIL} / {FACULTY_PASSWORD} ({SAMPLE_FACULTY_EMPLOYEE_ID})")
    print(f"  Parent:  {PARENT_EMAIL} / {PARENT_PASSWORD} (guardian of {STUDENT_ROLLS[0][0]})")
    for roll, name in STUDENT_ROLLS:
        print(f"  Student: {roll} / {STUDENT_PASSWORD} ({name})")
    if mode == "minimal":
        print(f"Institution 2 ({INSTITUTION_2_NAME}):")
        print(f"  Admin:   {ADMIN_2_EMAIL} / {ADMIN_2_PASSWORD}")
        print(f"  Student: {STUDENT_2_ROLL} / {STUDENT_PASSWORD}")
    print(f"ML predictions stored: {prediction_count}")
    print("Other students sign in with their roll number and the student password.")
    print("Other parents sign in with p-<roll>@demo.edu and the parent password.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed local development data")
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Small CSE slice plus a second institution (for tests)",
    )
    args = parser.parse_args()
    seed(mode="minimal" if args.minimal else "large")
