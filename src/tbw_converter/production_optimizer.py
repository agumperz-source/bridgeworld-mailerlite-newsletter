"""Conservative production HTML optimizers.

The functions here are intentionally small and measurable. They avoid structural
rewrites and report byte savings for each transform.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import re
from pathlib import Path
from typing import Callable

from .fingerprints import fingerprint_protected_regions


STYLE_BLOCK_RE = re.compile(r"(<style\b[^>]*>)(.*?)(</style>)", re.I | re.S)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
STYLE_ATTR_RE = re.compile(r"\sstyle=(['\"])(.*?)\1", re.I | re.S)


@dataclass(frozen=True)
class OptimizationResult:
    html: str
    report: dict


def optimize_production_html(html: str) -> OptimizationResult:
    """Apply Tier 1-safe production optimizations and return a report."""
    before_fingerprints = fingerprint_protected_regions(html)
    transforms: list[tuple[str, Callable[[str], str]]] = [
        ("minify_style_blocks", minify_style_blocks),
        ("minify_style_attributes", minify_style_attributes),
    ]
    current = html
    steps = []
    for name, transform in transforms:
        before = len(current.encode("utf-8"))
        current = transform(current)
        after = len(current.encode("utf-8"))
        steps.append({"name": name, "before_bytes": before, "after_bytes": after, "bytes_saved": before - after})
    after_fingerprints = fingerprint_protected_regions(current)
    report = {
        "before_bytes": len(html.encode("utf-8")),
        "after_bytes": len(current.encode("utf-8")),
        "bytes_saved": len(html.encode("utf-8")) - len(current.encode("utf-8")),
        "steps": steps,
        "protected_fingerprints_changed": before_fingerprints != after_fingerprints,
        "before_fingerprints": before_fingerprints,
        "after_fingerprints": after_fingerprints,
    }
    return OptimizationResult(html=current, report=report)


def minify_style_blocks(html: str) -> str:
    """Remove CSS comments and formatting whitespace inside style blocks only."""

    def repl(match: re.Match[str]) -> str:
        open_tag, css, close_tag = match.groups()
        css = CSS_COMMENT_RE.sub("", css)
        css = re.sub(r"\s+", " ", css)
        css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
        css = css.replace(";}", "}")
        return f"{open_tag}{css.strip()}{close_tag}"

    return STYLE_BLOCK_RE.sub(repl, html)


def minify_style_attributes(html: str) -> str:
    """Remove formatting whitespace inside inline style attributes.

    This preserves declaration order and values. It does not deduplicate,
    hoist, or remove properties, which keeps the transform suitable for
    Outlook-sensitive production markup.
    """

    def repl(match: re.Match[str]) -> str:
        quote, css = match.groups()
        css = re.sub(r"\s+", " ", css.strip())
        css = re.sub(r"\s*([:;,])\s*", r"\1", css)
        css = css.rstrip(";")
        return f" style={quote}{css}{quote}"

    return STYLE_ATTR_RE.sub(repl, html)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_path")
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    source = Path(args.html_path)
    result = optimize_production_html(source.read_text(encoding="utf-8-sig"))
    if args.output:
        Path(args.output).write_text(result.html, encoding="utf-8", newline="\n")
    if args.json:
        print(json.dumps(result.report, indent=2, sort_keys=True))
    else:
        print(f"before={result.report['before_bytes']} after={result.report['after_bytes']} saved={result.report['bytes_saved']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
