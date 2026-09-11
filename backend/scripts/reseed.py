"""Drop all tables, recreate schema, and run full seed."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import Base, engine
from app.ml.model_loader import model_loader
from scripts.seed import seed


def reseed(scale: int = 100, cse_demo: bool = False):
    print("Dropping and recreating schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    if not model_loader.is_loaded:
        model_loader.load()

    mode = "cse-demo" if cse_demo else f"scale={scale}"
    print(f"Running seed ({mode})...")
    seed(force=True, scale=scale, cse_demo=cse_demo)
    print("Reseed complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drop, recreate, and seed database")
    parser.add_argument("--scale", type=int, default=100, help="Student scale for bulk seed")
    parser.add_argument(
        "--cse-demo",
        action="store_true",
        help="Seed CSE, ECE, IST branches (60 students each, 4 semesters)",
    )
    args = parser.parse_args()
    reseed(scale=args.scale, cse_demo=args.cse_demo)
