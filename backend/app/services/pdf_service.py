"""HTML to PDF rendering with WeasyPrint primary and xhtml2pdf fallback."""

from __future__ import annotations

import logging
import os
import platform
from io import BytesIO
from pathlib import Path

logger = logging.getLogger(__name__)


def _configure_weasyprint_library_path() -> None:
    """Help WeasyPrint find Homebrew libraries on macOS."""
    if platform.system() != "Darwin":
        return
    brew_lib = Path("/opt/homebrew/lib")
    if not brew_lib.is_dir():
        return
    current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    lib_path = str(brew_lib)
    if lib_path not in current.split(":"):
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
            f"{lib_path}:{current}" if current else lib_path
        )


def _render_with_weasyprint(html: str) -> bytes | None:
    _configure_weasyprint_library_path()
    try:
        from weasyprint import HTML

        return HTML(string=html).write_pdf()
    except (ImportError, OSError) as exc:
        logger.info("WeasyPrint unavailable, using fallback PDF renderer: %s", exc)
        return None


def _render_with_xhtml2pdf(html: str) -> bytes:
    from xhtml2pdf import pisa

    buffer = BytesIO()
    status = pisa.CreatePDF(src=html, dest=buffer, encoding="utf-8")
    if status.err:
        raise RuntimeError("xhtml2pdf failed to render report HTML")
    return buffer.getvalue()


def render_pdf(html: str) -> bytes:
    """Render report HTML to PDF bytes."""
    pdf = _render_with_weasyprint(html)
    if pdf is not None:
        return pdf
    return _render_with_xhtml2pdf(html)
