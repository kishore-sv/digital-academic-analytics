"""Drop all tables, recreate schema, and run the development seed."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.models  # noqa: F401 — register models on Base.metadata
from app.core.database import Base, engine
from app.ml.model_loader import model_loader
from scripts.seed import seed


def reseed(minimal: bool = False) -> None:
    print("Dropping and recreating schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    if not model_loader.is_loaded:
        model_loader.load()

    mode = "minimal" if minimal else "large"
    print(f"Running seed ({mode})...")
    seed(mode=mode)
    print("Reseed complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drop, recreate, and seed the database")
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Small CSE slice and a second institution (pytest). Default is 2,400 students.",
    )
    args = parser.parse_args()
    reseed(minimal=args.minimal)
