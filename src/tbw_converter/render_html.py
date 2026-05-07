"""Render canonical JSON into authoring HTML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .validation_core import render_authoring_html, validate_newsletter_json


def render_html(newsletter: dict[str, Any], template_path: str | Path = "templates/authoring_canonical.html") -> str:
    """Render authoring HTML from validated canonical JSON.

    Rendering is intentionally limited to editable/content regions and does not
    infer article type, bridge meaning, or layout from source HTML.
    """
    report = validate_newsletter_json(newsletter)
    if report.hard_fails() or report.human_review():
        details = "; ".join(f"{item.validator}:{item.code}" for item in report.hard_fails() + report.human_review())
        raise ValueError(f"Newsletter JSON is not renderable: {details}")
    template_html = Path(template_path).read_text(encoding="utf-8-sig")
    return render_authoring_html(newsletter, template_html)
