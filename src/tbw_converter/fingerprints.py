"""Protected-region fingerprinting for production/rendering stability."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RegionSpec:
    name: str
    start: str
    end: str
    required_tokens: tuple[str, ...] = ()
    occurrence: str = "first"


REGIONS = (
    RegionSpec("newsletter_identity", 'class="tbw-newsletter-identity"', "</td>", ("Times New Roman",)),
    RegionSpec("problem_solution_heading", 'class="tbw-section-heading"', "</table>", ("tbw-section-heading-cell",)),
    RegionSpec("hand_geometry", 'class="tbw-hand-stage"', "</table>", ("tbw-hand-table", "hlabel")),
    RegionSpec("mso_auction", "<!--[if mso]>", "<![endif]-->", ("tbw-auction", "mso-line-height-rule"), "contains_auction"),
    RegionSpec("stay_connected", 'class="tbw-stay-title"', "</table>", ("Stay Connected", "Times New Roman")),
    RegionSpec("footer", 'class="tbw-footer', "</table>", ("border-top:2px solid #555",)),
)


def fingerprint_protected_regions(html: str) -> dict[str, Any]:
    """Return normalized hashes for known protected regions."""
    regions = []
    for spec in REGIONS:
        extract = extract_region(html, spec)
        normalized = normalize_region(extract)
        regions.append(
            {
                "name": spec.name,
                "present": bool(extract),
                "bytes": len(extract.encode("utf-8")),
                "sha256": sha256(normalized.encode("utf-8")).hexdigest() if extract else "",
                "required_tokens_present": {token: token in extract for token in spec.required_tokens},
            }
        )
    return {"regions": regions}


def validate_protected_fingerprints(html: str) -> list[str]:
    """Return validation errors for missing protected regions/tokens."""
    report = fingerprint_protected_regions(html)
    errors: list[str] = []
    for region in report["regions"]:
        if not region["present"]:
            errors.append(f"missing protected region: {region['name']}")
            continue
        for token, present in region["required_tokens_present"].items():
            if not present:
                errors.append(f"protected region {region['name']} missing token: {token}")
    return errors


def extract_region(html: str, spec: RegionSpec) -> str:
    if spec.occurrence == "contains_auction":
        for match in re.finditer(re.escape(spec.start) + r".*?" + re.escape(spec.end), html, re.I | re.S):
            candidate = match.group(0)
            if "auction" in candidate.lower():
                return candidate
        return ""
    start_index = html.find(spec.start)
    if start_index == -1:
        return ""
    end_index = html.find(spec.end, start_index)
    if end_index == -1:
        return html[start_index:]
    return html[start_index : end_index + len(spec.end)]


def normalize_region(html: str) -> str:
    value = re.sub(r">\s+<", "><", html)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fingerprint_file(path: str | Path) -> dict[str, Any]:
    return fingerprint_protected_regions(Path(path).read_text(encoding="utf-8-sig"))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("html_path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = fingerprint_file(args.html_path)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for region in report["regions"]:
            print(f"{region['name']}: present={region['present']} bytes={region['bytes']} sha256={region['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
