"""Production HTML size analysis helpers.

This module measures where bytes are going without changing markup. It is used
to choose safe, modular production reductions before touching protected regions.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any


STYLE_ATTR_RE = re.compile(r"\sstyle=(['\"])(.*?)\1", re.I | re.S)
CLASS_ATTR_RE = re.compile(r"\sclass=(['\"])(.*?)\1", re.I | re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
MSO_RE = re.compile(r"<!--\[if mso\].*?<!\[endif\]-->", re.I | re.S)
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
IMG_SRC_RE = re.compile(r"\ssrc=(['\"])(.*?)\1", re.I | re.S)
TABLE_ATTR_RE = re.compile(r"\s(?:width|height|border|cellpadding|cellspacing|align|valign|bgcolor|role)=(['\"])[^'\"]*\1", re.I)


@dataclass(frozen=True)
class SizeBucket:
    name: str
    bytes: int
    count: int


def analyze_html_size(html: str) -> dict[str, Any]:
    """Return deterministic size buckets and repeated-fragment hints."""
    total = byte_len(html)
    comments = COMMENT_RE.findall(html)
    mso_blocks = MSO_RE.findall(html)
    style_blocks = STYLE_BLOCK_RE.findall(html)
    style_attrs = [match.group(0) for match in STYLE_ATTR_RE.finditer(html)]
    class_attrs = [match.group(0) for match in CLASS_ATTR_RE.finditer(html)]
    table_attrs = [match.group(0) for match in TABLE_ATTR_RE.finditer(html)]
    img_srcs = [match.group(0) for match in IMG_SRC_RE.finditer(html)]
    whitespace_between_tags = re.findall(r">\s+<", html)
    repeated_styles = repeated_fragments(style_attrs)
    repeated_classes = repeated_fragments(class_attrs)

    buckets = [
        SizeBucket("total", total, 1),
        SizeBucket("comments", sum(byte_len(item) for item in comments), len(comments)),
        SizeBucket("mso_blocks", sum(byte_len(item) for item in mso_blocks), len(mso_blocks)),
        SizeBucket("style_blocks", sum(byte_len(item) for item in style_blocks), len(style_blocks)),
        SizeBucket("style_attributes", sum(byte_len(item) for item in style_attrs), len(style_attrs)),
        SizeBucket("class_attributes", sum(byte_len(item) for item in class_attrs), len(class_attrs)),
        SizeBucket("table_layout_attributes", sum(byte_len(item) for item in table_attrs), len(table_attrs)),
        SizeBucket("image_src_attributes", sum(byte_len(item) for item in img_srcs), len(img_srcs)),
        SizeBucket("intertag_whitespace", sum(byte_len(item) - 2 for item in whitespace_between_tags), len(whitespace_between_tags)),
    ]
    return {
        "total_bytes": total,
        "buckets": [bucket.__dict__ for bucket in buckets],
        "top_repeated_style_attributes": repeated_styles[:15],
        "top_repeated_class_attributes": repeated_classes[:15],
        "asset_url_counts": asset_url_counts(html),
    }


def analyze_file(path: str | Path) -> dict[str, Any]:
    html = Path(path).read_text(encoding="utf-8-sig")
    return analyze_html_size(html)


def repeated_fragments(items: list[str]) -> list[dict[str, Any]]:
    counts = Counter(items)
    repeated = []
    for text, count in counts.most_common():
        if count < 2:
            continue
        repeated.append(
            {
                "count": count,
                "bytes_each": byte_len(text),
                "bytes_total": byte_len(text) * count,
                "fragment": compact(text),
            }
        )
    return repeated


def asset_url_counts(html: str) -> dict[str, int]:
    urls = re.findall(r"https://agumperz-source\.github\.io/bw/a/[A-Za-z0-9_.-]+", html)
    return dict(sorted(Counter(urls).items()))


def compact(text: str, max_len: int = 180) -> str:
    value = re.sub(r"\s+", " ", text).strip()
    if len(value) <= max_len:
        return value
    return value[: max_len - 3] + "..."


def byte_len(text: str) -> int:
    return len(text.encode("utf-8"))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("html_path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = analyze_file(args.html_path)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"total_bytes={report['total_bytes']}")
        for bucket in report["buckets"]:
            print(f"{bucket['name']}: bytes={bucket['bytes']} count={bucket['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
