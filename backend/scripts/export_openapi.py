#!/usr/bin/env python3
"""Export OpenAPI JSON from the FastAPI app.

Usage (from backend/):
    uv run python scripts/export_openapi.py
    uv run python scripts/export_openapi.py ../docs/openapi.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = BACKEND_ROOT.parent / "docs" / "openapi.json"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    from app.main import app

    payload = app.openapi()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
