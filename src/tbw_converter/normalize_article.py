"""Normalize extracted source objects into canonical newsletter JSON."""

from __future__ import annotations

from typing import Any


class NormalizationUnavailable(RuntimeError):
    """Raised when source data lacks deterministic semantic extraction."""


def normalize_article(extracted_text: Any):
    """Fail closed unless a deterministic extracted semantic object is supplied."""
    raise NormalizationUnavailable(
        "Article normalization requires deterministic source objects produced by the extraction layer. "
        "Raw text is not sufficient to infer bridge facts."
    )
