#!/usr/bin/env python3
"""Generate markdown API reference from the FastAPI OpenAPI schema.

Usage (from backend/):
    uv run python scripts/generate_api_docs.py

Writes: ../docs/api-reference.generated.md
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

# backend/
BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
OUTPUT = REPO_ROOT / "docs" / "api-reference.generated.md"


def _ref_name(ref: str) -> str:
    return ref.split("/")[-1]


def _schema_summary(schema: dict, components: dict) -> str:
    if not schema:
        return "_none_"
    if "$ref" in schema:
        return f"`{_ref_name(schema['$ref'])}`"
    if schema.get("type") == "array" and "items" in schema:
        return f"array of {_schema_summary(schema['items'], components)}"
    return f"`{json.dumps(schema, sort_keys=True)[:120]}...`" if len(json.dumps(schema)) > 120 else f"`{schema.get('type', 'object')}`"


def _resolve_schema(schema: dict | None, components: dict) -> dict | None:
    if not schema:
        return None
    if "$ref" in schema:
        name = _ref_name(schema["$ref"])
        return components.get("schemas", {}).get(name)
    return schema


def _properties_table(schema: dict | None, components: dict) -> str:
    resolved = _resolve_schema(schema, components)
    if not resolved:
        return ""
    props = resolved.get("properties") or {}
    required = set(resolved.get("required") or [])
    if not props:
        return ""
    lines = ["| Field | Type | Required | Description |", "|-------|------|----------|-------------|"]
    for key, meta in props.items():
        typ = meta.get("type") or (_ref_name(meta["$ref"]) if "$ref" in meta else "object")
        if meta.get("anyOf"):
            typ = " | ".join(
                m.get("type") or (_ref_name(m["$ref"]) if "$ref" in m else "?")
                for m in meta["anyOf"]
            )
        desc = (meta.get("description") or meta.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| `{key}` | {typ} | {'yes' if key in required else 'no'} | {desc} |"
        )
    return "\n".join(lines)


def main() -> None:
    from app.main import app

    spec = app.openapi()
    paths = spec.get("paths", {})
    components = spec.get("components", {})

    by_tag: dict[str, list[tuple[str, str, dict]]] = defaultdict(list)

    for path, methods in sorted(paths.items()):
        for method, operation in methods.items():
            if method.startswith("x-"):
                continue
            tags = operation.get("tags") or ["default"]
            tag = tags[0]
            by_tag[tag].append((method.upper(), path, operation))

    lines: list[str] = [
        "# API Reference (generated)",
        "",
        "_Auto-generated from the FastAPI OpenAPI schema. Do not edit by hand._",
        "",
        "Regenerate:",
        "",
        "```bash",
        "cd backend && uv run python scripts/generate_api_docs.py",
        "```",
        "",
        "**Interactive UI:** [Swagger](/docs) · [ReDoc](/redoc) (with `uvicorn` on port 8000)",
        "",
        f"**Base path:** `{spec.get('servers', [{}])[0].get('url', '/api/v1')}`",
        "",
    ]

    tag_order = [t["name"] for t in (spec.get("tags") or [])]
    for tag in sorted(by_tag.keys(), key=lambda t: tag_order.index(t) if t in tag_order else 999):
        lines.append(f"## {tag}")
        lines.append("")
        tag_desc = next(
            (t.get("description", "") for t in (spec.get("tags") or []) if t.get("name") == tag),
            "",
        )
        if tag_desc:
            lines.append(tag_desc)
            lines.append("")

        for method, path, operation in sorted(by_tag[tag], key=lambda x: (x[1], x[0])):
            summary = operation.get("summary") or operation.get("operationId", "")
            description = (operation.get("description") or "").strip()
            lines.append(f"### `{method}` `{path}`")
            lines.append("")
            if summary:
                lines.append(f"**Summary:** {summary}")
                lines.append("")
            if description:
                lines.append(description)
                lines.append("")

            params = operation.get("parameters") or []
            if params:
                lines.append("**Query / path parameters**")
                lines.append("")
                lines.append("| Name | In | Required | Type |")
                lines.append("|------|-----|----------|------|")
                for p in params:
                    schema = p.get("schema") or {}
                    typ = schema.get("type") or (
                        _ref_name(schema["$ref"]) if "$ref" in schema else "string"
                    )
                    lines.append(
                        f"| `{p.get('name')}` | {p.get('in')} | "
                        f"{'yes' if p.get('required') else 'no'} | {typ} |"
                    )
                lines.append("")

            request_body = operation.get("requestBody")
            if request_body:
                content = request_body.get("content", {}).get("application/json", {})
                schema = content.get("schema")
                lines.append("**Request body** (`application/json`)")
                lines.append("")
                table = _properties_table(schema, components)
                if table:
                    lines.append(table)
                else:
                    lines.append(_schema_summary(schema, components))
                lines.append("")

            responses = operation.get("responses") or {}
            lines.append("**Responses**")
            lines.append("")
            for status, resp in sorted(responses.items(), key=lambda x: x[0]):
                content = resp.get("content", {}).get("application/json", {})
                schema = content.get("schema")
                desc = resp.get("description", "")
                body = _schema_summary(schema, components) if schema else "_empty_"
                lines.append(f"- **{status}** — {desc}: {body}")
            lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
