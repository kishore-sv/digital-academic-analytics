"""Parse uploaded CSV/XLSX files into row dictionaries."""

from __future__ import annotations

import csv
import io
from typing import Any

import pandas as pd


def parse_upload(filename: str, content: bytes) -> tuple[list[str], list[dict[str, str]]]:
    lower = filename.lower()
    if lower.endswith(".csv"):
        return _parse_csv(content)
    if lower.endswith(".xlsx"):
        return _parse_xlsx(content)
    raise ValueError("Unsupported file type. Use CSV or XLSX.")


def _parse_csv(content: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV file has no header row.")
    headers = [h.strip() for h in reader.fieldnames if h]
    rows: list[dict[str, str]] = []
    for raw in reader:
        row = {k.strip(): _cell(v) for k, v in raw.items() if k and k.strip()}
        if any(row.values()):
            rows.append(row)
    return headers, rows


def _parse_xlsx(content: bytes) -> tuple[list[str], list[dict[str, str]]]:
    df = pd.read_excel(io.BytesIO(content), dtype=str)
    df = df.fillna("")
    headers = [str(c).strip() for c in df.columns]
    rows: list[dict[str, str]] = []
    for record in df.to_dict(orient="records"):
        row = {str(k).strip(): _cell(v) for k, v in record.items()}
        if any(row.values()):
            rows.append(row)
    return headers, rows


def _cell(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
