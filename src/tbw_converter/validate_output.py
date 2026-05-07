"""Validation entrypoints for newsletter JSON, HTML, and package checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .validation_core import (
    ValidationReport,
    export_production_html,
    validate_newsletter_json,
    validate_package,
    validate_production_html,
)


def validate_output(article: dict[str, Any], html: str) -> ValidationReport:
    """Validate article JSON and rendered HTML without mutating either input."""
    report = validate_newsletter_json(article)
    validate_production_html(html, report, "rendered_html")
    return report


def validate_package_root(path: str | Path = ".") -> ValidationReport:
    """Compatibility wrapper for callers that want an explicit root name."""
    return validate_package(path)
