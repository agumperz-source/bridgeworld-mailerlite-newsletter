"""Fail-closed PDF extraction boundary.

The package requires rasterization-first extraction with OCR confidence and
source inventory tracking. Until those dependencies are explicitly installed
and wired, extraction must fail rather than guess bridge facts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceInventoryItem:
    source_id: str
    path: str
    classification: str
    status: str
    message: str


class ExtractionUnavailable(RuntimeError):
    """Raised when deterministic raster/OCR extraction is unavailable."""


def build_source_inventory(paths: list[str | Path]) -> list[SourceInventoryItem]:
    """Create a conservative source inventory without classifying content."""
    inventory: list[SourceInventoryItem] = []
    for index, path in enumerate(paths, start=1):
        source_path = Path(path)
        inventory.append(
            SourceInventoryItem(
                source_id=f"source_{index}",
                path=str(source_path),
                classification="unknown",
                status="human_review_required",
                message="Content classification requires raster/OCR extraction and human-safe confidence checks.",
            )
        )
    return inventory


def extract_pdf(path: str | Path):
    """Fail closed until rasterization-first extraction is implemented."""
    raise ExtractionUnavailable(
        f"Cannot extract {path}: rasterization-first OCR extraction is not implemented. "
        "Extraction must fail rather than infer bridge facts."
    )
