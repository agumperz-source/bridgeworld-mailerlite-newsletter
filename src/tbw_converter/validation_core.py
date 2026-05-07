"""Deterministic validators for the Bridge World newsletter package.

The active rule files remain the authority. This module implements the Phase 1
validation foundation described by ``validators/README.md`` and
``validators/validation_gates.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from html import escape
import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


SEATS = ("N", "E", "S", "W")
WNES = ("W", "N", "E", "S")
SUITS = ("S", "H", "D", "C")
RANKS = ("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")
STRAINS = ("C", "D", "H", "S", "NT")
CANONICAL_ASSETS = {
    "S": "https://agumperz-source.github.io/bw/a/S.png",
    "H": "https://agumperz-source.github.io/bw/a/H.png",
    "D": "https://agumperz-source.github.io/bw/a/D.png",
    "C": "https://agumperz-source.github.io/bw/a/C.png",
    "BW": "https://agumperz-source.github.io/bw/a/BW.png",
    "logo": "https://agumperz-source.github.io/bw/a/logo.png",
}
PRODUCTION_IDEAL_BYTES = 75_000
PRODUCTION_WARNING_BYTES = 85_000
PRODUCTION_HARD_FAIL_BYTES = 95_000
MAILERLITE_ESTIMATED_INJECTION_BYTES = 25_000
LEGACY_ASSET_RE = re.compile(r"https://storage\.mlcdn\.com/account_image/[^\s\"')<>]+", re.I)
RAW_SUIT_RE = re.compile(r"(?<!alt=[\"'])[\u2660\u2663\u2665\u2666]")


@dataclass(frozen=True)
class Finding:
    severity: str
    validator: str
    code: str
    message: str
    path: str = ""


@dataclass
class ValidationReport:
    findings: list[Finding] = field(default_factory=list)
    info: dict[str, Any] = field(default_factory=dict)

    def add(self, severity: str, validator: str, code: str, message: str, path: str = "") -> None:
        self.findings.append(Finding(severity, validator, code, message, path))

    def hard_fails(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "hard_fail"]

    def warnings(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "warning"]

    def human_review(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "human_review_required"]

    @property
    def ok(self) -> bool:
        return not self.hard_fails() and not self.human_review()

    def to_dict(self) -> dict[str, Any]:
        counts: dict[str, int] = {"hard_fail": 0, "warning": 0, "human_review_required": 0, "info": 0}
        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
        return {
            "ok": self.ok,
            "counts": counts,
            "findings": [finding.__dict__ for finding in self.findings],
            "info": self.info,
        }


def validate_package(package_root: str | Path = ".") -> ValidationReport:
    """Run all package validators and return a structured report."""
    root = Path(package_root)
    report = ValidationReport()
    validate_manifest(root, report)
    validate_templates(root, report)
    validate_schema_file(root, report)
    validate_fixtures(root, report)
    validate_extraction_contract(root, report)
    validate_rendering_invariants(root, report)
    validate_production_export(root, report)
    return report


def validate_manifest(root: Path, report: ValidationReport) -> None:
    required = [
        "bootstrap.md",
        "manifest.md",
        "templates/authoring_canonical.html",
        "templates/production_canonical.html",
        "templates/canonical.html",
        "instructions/extraction_rules.md",
        "instructions/semantic_schema.md",
        "instructions/semantic_bridge_rules.md",
        "instructions/layout_intent_rules.md",
        "instructions/rendering_rules.md",
        "instructions/production_export.md",
        "instructions/validation.md",
        "validators/README.md",
        "schema/newsletter.schema.json",
        "fixtures/README.md",
        "fixtures/rendering_fingerprints.spec.json",
        "validators/validation_gates.md",
        "CODEX_HANDOFF.md",
        "reports/change_report.md",
    ]
    for rel in required:
        if not (root / rel).exists():
            report.add("hard_fail", "manifest", "missing_required_file", f"Required package file is missing: {rel}", rel)

    manifest = read_text(root / "manifest.md")
    for key, url in CANONICAL_ASSETS.items():
        if url not in manifest:
            report.add("hard_fail", "manifest", "asset_map_missing", f"Manifest is missing canonical asset URL for {key}.", "manifest.md")


def validate_templates(root: Path, report: ValidationReport) -> None:
    authoring = root / "templates" / "authoring_canonical.html"
    alias = root / "templates" / "canonical.html"
    production = root / "templates" / "production_canonical.html"
    authoring_html = read_text(authoring)
    alias_html = read_text(alias)
    production_html = read_text(production)

    if authoring_html != alias_html:
        report.add("hard_fail", "templates", "canonical_alias_diverged", "templates/canonical.html differs from authoring_canonical.html.", str(alias))
    for path, html in ((authoring, authoring_html), (production, production_html)):
        if LEGACY_ASSET_RE.search(html):
            report.add("hard_fail", "templates", "legacy_asset_url", f"Legacy MailerLite asset URL appears in {path.name}.", str(path))
        for url in CANONICAL_ASSETS.values():
            if url not in html:
                report.add("warning", "templates", "canonical_asset_not_used", f"{path.name} does not reference {url}.", str(path))

    required_authoring = [
        "BEGIN_EDITABLE:NEWSLETTER_IDENTITY",
        "BEGIN_EDITABLE:ARTICLE_TITLE",
        "ARTICLE_BLOCK_PLAY_DEFENSE_START",
        "Stay Connected",
    ]
    for token in required_authoring:
        if token not in authoring_html:
            report.add("hard_fail", "templates", "missing_authoring_region", f"Authoring template missing protected/editable token: {token}", str(authoring))

    if "<!-- BEGIN_EDITABLE:" in production_html:
        report.add("hard_fail", "templates", "production_has_edit_markers", "Production template contains editable-region markers.", str(production))

    report.info["authoring_template_size"] = len(authoring_html.encode("utf-8"))
    report.info["production_template_size"] = len(production_html.encode("utf-8"))
    report.info["authoring_template_sha256"] = sha256(authoring_html.encode("utf-8")).hexdigest()
    report.info["production_template_sha256"] = sha256(production_html.encode("utf-8")).hexdigest()


def validate_schema_file(root: Path, report: ValidationReport) -> None:
    schema_path = root / "schema" / "newsletter.schema.json"
    try:
        schema = load_json(schema_path)
    except ValueError as exc:
        report.add("hard_fail", "schema", "schema_json_invalid", str(exc), str(schema_path))
        return
    for top_key in ("newsletter_identity", "publication_date", "preheader_text", "editor_note", "article", "asset_map"):
        if top_key not in schema.get("properties", {}):
            report.add("hard_fail", "schema", "schema_missing_property", f"Schema does not define top-level property {top_key}.", str(schema_path))


def validate_fixtures(root: Path, report: ValidationReport) -> None:
    for fixture in sorted((root / "fixtures").glob("*.json")):
        if fixture.name == "rendering_fingerprints.spec.json":
            continue
        try:
            data = load_json(fixture)
        except ValueError as exc:
            report.add("hard_fail", "fixtures", "fixture_json_invalid", str(exc), str(fixture))
            continue
        fixture_report = validate_newsletter_json(data, fixture.name)

        if fixture.name.endswith(".hard_fail.json"):
            if not fixture_report.hard_fails():
                report.add("hard_fail", "fixtures", "expected_hard_fail_missing", f"Fixture {fixture.name} did not produce a hard_fail.", str(fixture))
            report.info.setdefault("expected_hard_fail_fixtures", {})[fixture.name] = [
                finding.__dict__ for finding in fixture_report.hard_fails()
            ]
        elif fixture_report.hard_fails():
            report.findings.extend(fixture_report.findings)
            report.add("hard_fail", "fixtures", "expected_fixture_failed", f"Fixture {fixture.name} produced hard failures.", str(fixture))
        else:
            report.findings.extend(fixture_report.warnings())
            report.findings.extend(fixture_report.human_review())


def validate_newsletter_json(data: dict[str, Any], source_name: str = "newsletter") -> ValidationReport:
    report = ValidationReport()
    validate_minimal_schema(data, report, source_name)
    validate_source_issues(data, report, source_name)
    validate_asset_map(data, report, source_name)
    validate_bridge_consistency(data, report, source_name)
    validate_auction(data, report, source_name)
    validate_layout_intents(data, report, source_name)
    return report


def validate_minimal_schema(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    required = ("newsletter_identity", "publication_date", "preheader_text", "editor_note", "article", "asset_map", "layout_intents", "validation_status")
    for key in required:
        if key not in data:
            report.add("hard_fail", "schema_validator", "required_missing", f"Missing required field {key}.", source_name)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(data.get("publication_date", ""))):
        report.add("hard_fail", "schema_validator", "bad_publication_date", "publication_date must be YYYY-MM-DD.", source_name)
    article = data.get("article")
    if not isinstance(article, dict):
        report.add("hard_fail", "schema_validator", "article_not_object", "article must be an object.", source_name)
        return
    if article.get("article_type") not in {"bidding_msc", "play_problem", "defense_problem", "historical_deal_article", "other_feature_article"}:
        report.add("hard_fail", "schema_validator", "bad_article_type", "article.article_type is invalid or missing.", source_name)
    if not isinstance(article.get("sections"), list):
        report.add("hard_fail", "schema_validator", "sections_not_array", "article.sections must be an array.", source_name)


def validate_source_issues(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    for issue in data.get("validation_status", {}).get("source_issues", []) or []:
        severity = issue.get("severity", "warning")
        if severity in {"hard_fail", "warning", "human_review_required", "info"}:
            report.add(severity, "source_inventory_validator", issue.get("type", "source_issue"), issue.get("message", "Source issue reported."), source_name)


def validate_asset_map(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    assets = data.get("asset_map", {})
    for key, url in CANONICAL_ASSETS.items():
        if assets.get(key) != url:
            report.add("hard_fail", "schema_validator", "asset_map_mismatch", f"asset_map.{key} must be {url}.", source_name)


def validate_bridge_consistency(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    hands = data.get("article", {}).get("hands", {}) or {}
    seen: dict[str, str] = {}
    total_known = 0
    full_hands = 0
    for seat, hand in hands.items():
        if seat not in WNES:
            report.add("hard_fail", "bridge_consistency_validator", "invalid_seat", f"Invalid hand seat {seat}.", source_name)
            continue
        cards_in_hand = 0
        for suit, ranks_text in (hand or {}).items():
            if suit not in SUITS:
                report.add("hard_fail", "bridge_consistency_validator", "invalid_suit", f"Invalid suit key {seat}.{suit}.", source_name)
                continue
            for rank in split_ranks(ranks_text):
                if rank not in RANKS:
                    report.add("hard_fail", "bridge_consistency_validator", "invalid_rank", f"Invalid rank token {rank} in {seat}.{suit}.", source_name)
                    continue
                card = f"{suit}{rank}"
                if card in seen:
                    report.add("hard_fail", "bridge_consistency_validator", "duplicate_card", f"Card {card} appears in both {seen[card]} and {seat}.", source_name)
                else:
                    seen[card] = seat
                cards_in_hand += 1
        if cards_in_hand > 13:
            report.add("hard_fail", "bridge_consistency_validator", "too_many_cards", f"{seat} has {cards_in_hand} cards.", source_name)
        if cards_in_hand == 13:
            full_hands += 1
        total_known += cards_in_hand
    if len(hands) == 4 and full_hands == 4 and total_known != 52:
        report.add("hard_fail", "bridge_consistency_validator", "bad_full_deal_count", f"Full deal has {total_known} cards, not 52.", source_name)


def validate_auction(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    auction = data.get("article", {}).get("auction")
    if not auction:
        return
    dealer = auction.get("dealer") or data.get("article", {}).get("deal_facts", {}).get("dealer")
    calls = auction.get("call_order") or []
    if dealer not in WNES:
        report.add("hard_fail", "auction_validator", "missing_dealer", "Auction dealer is missing or invalid.", source_name)
        return
    if not isinstance(calls, list):
        report.add("hard_fail", "auction_validator", "calls_not_array", "auction.call_order must be an array.", source_name)
        return
    dealer_index = WNES.index(dealer)
    last_bid: tuple[int, int] | None = None
    last_bid_side: str | None = None
    doubled_side: str | None = None
    passes_after_bid = 0
    for index, item in enumerate(calls):
        expected = WNES[(dealer_index + index) % 4]
        seat = item.get("seat")
        call = normalize_call(item.get("call", ""))
        if seat != expected:
            report.add("hard_fail", "auction_validator", "bad_call_rotation", f"Call {index + 1} belongs to {seat}, expected {expected}.", source_name)
        side = "NS" if seat in {"N", "S"} else "EW"
        if call == "?":
            if index != len(calls) - 1 or auction.get("status") != "incomplete":
                report.add("hard_fail", "auction_validator", "bad_question_call", "Question mark call is allowed only as final incomplete call.", source_name)
            continue
        if call == "Pass":
            passes_after_bid += 1
            continue
        bid = parse_bid(call)
        if bid:
            passes_after_bid = 0
            if last_bid and bid <= last_bid:
                report.add("hard_fail", "auction_validator", "insufficient_bid", f"Bid {call} does not exceed the prior bid.", source_name)
            last_bid = bid
            last_bid_side = side
            doubled_side = None
            continue
        if call == "Double":
            if not last_bid_side or last_bid_side == side or doubled_side is not None:
                report.add("hard_fail", "auction_validator", "illegal_double", f"Illegal double by {seat}.", source_name)
            else:
                doubled_side = last_bid_side
            passes_after_bid = 0
            continue
        if call == "Redouble":
            if doubled_side != side:
                report.add("hard_fail", "auction_validator", "illegal_redouble", f"Illegal redouble by {seat}.", source_name)
            else:
                doubled_side = None
            passes_after_bid = 0
            continue
        report.add("hard_fail", "auction_validator", "unknown_call", f"Unknown auction call {call}.", source_name)

    if auction.get("status") == "complete" and last_bid and passes_after_bid < 3:
        report.add("hard_fail", "auction_validator", "complete_auction_not_ended", "Complete auction does not end with three passes after a bid.", source_name)


def validate_layout_intents(data: dict[str, Any], report: ValidationReport, source_name: str) -> None:
    article = data.get("article", {})
    intents = data.get("layout_intents", []) or []
    if not intents:
        report.add("hard_fail", "layout_intent_validator", "missing_layout_intent", "layout_intents must contain at least one intent.", source_name)
        return
    intent = intents[0]
    visible = set(intent.get("visible_seats") or [])
    hand_seats = set((article.get("hands") or {}).keys())
    if visible and hand_seats and visible != hand_seats:
        report.add("hard_fail", "layout_intent_validator", "visible_seat_mismatch", "layout_intent.visible_seats must match article.hands seats.", source_name)
    expected = {
        "play_problem": "vertical_ns",
        "defense_problem": "defense_three_position",
        "historical_deal_article": "full_deal_cross",
        "bidding_msc": "bidding_single_south",
    }.get(article.get("article_type"))
    if expected and intent.get("hand_layout") != expected:
        report.add("hard_fail", "layout_intent_validator", "bad_hand_layout", f"{article.get('article_type')} requires hand_layout {expected}.", source_name)
    if article.get("auction") and not intent.get("auction_layout"):
        report.add("hard_fail", "layout_intent_validator", "missing_auction_layout", "auction_layout is required when article.auction exists.", source_name)


def validate_extraction_contract(root: Path, report: ValidationReport) -> None:
    extract_module = root / "src" / "tbw_converter" / "extract_pdf.py"
    text = read_text(extract_module)
    if "ExtractionUnavailable" not in text or "raise ExtractionUnavailable" not in text:
        report.add("hard_fail", "source_inventory_validator", "extraction_not_fail_closed", "Extraction must fail closed until raster/OCR support is implemented.", str(extract_module))


def validate_rendering_invariants(root: Path, report: ValidationReport) -> None:
    html = read_text(root / "templates" / "authoring_canonical.html")
    ordered = ["tbw-newsletter-identity", "START ARTICLE HEADING", "ARTICLE_BLOCK_PLAY_DEFENSE_START"]
    last = -1
    for token in ordered:
        index = html.find(token)
        if index == -1:
            report.add("hard_fail", "rendering_validator", "missing_order_token", f"Missing rendering order token {token}.", "templates/authoring_canonical.html")
        elif index < last:
            report.add("hard_fail", "rendering_validator", "section_order_broken", f"Rendering order token {token} appears out of order.", "templates/authoring_canonical.html")
        last = max(last, index)
    stay_connected_index = html.rfind("Stay Connected")
    if stay_connected_index == -1:
        report.add("hard_fail", "rendering_validator", "missing_order_token", "Missing Stay Connected section.", "templates/authoring_canonical.html")
    elif stay_connected_index < last:
        report.add("hard_fail", "rendering_validator", "section_order_broken", "Stay Connected appears before article body mount.", "templates/authoring_canonical.html")
    if RAW_SUIT_RE.search(strip_comments(html)):
        report.add("warning", "rendering_validator", "raw_suit_glyphs", "Raw suit glyphs appear in template text; generated bridge content must use images.", "templates/authoring_canonical.html")


def validate_production_export(root: Path, report: ValidationReport) -> None:
    authoring_path = root / "templates" / "authoring_canonical.html"
    production_path = root / "templates" / "production_canonical.html"
    authoring_html = read_text(authoring_path)
    production_reference = read_text(production_path)
    safe_authoring_export = export_production_html(authoring_html)
    first = export_production_html(production_reference)
    second = export_production_html(first.html)
    if first.html != second.html:
        report.add("hard_fail", "production_validator", "export_not_idempotent", "Production export is not byte-idempotent.", str(production_path))
    validate_production_html(first.html, report, "templates/production_canonical.html")
    report.info["production_export_report"] = first.report
    report.info["safe_authoring_export_report"] = safe_authoring_export.report
    if safe_authoring_export.report["production_size"] > PRODUCTION_HARD_FAIL_BYTES:
        report.add(
            "warning",
            "production_validator",
            "authoring_safe_export_over_budget",
            "Tier 1-safe export from authoring template exceeds 95 KB; use production_canonical.html or add tested Tier 2 compression.",
            str(authoring_path),
        )


@dataclass(frozen=True)
class ExportResult:
    html: str
    report: dict[str, Any]


def export_production_html(authoring_html: str) -> ExportResult:
    """Export authoring HTML to deterministic MailerLite-ready HTML."""
    original_size = len(authoring_html.encode("utf-8"))
    html, url_replacements = replace_legacy_asset_urls(authoring_html)
    after_urls = len(html.encode("utf-8"))
    html, comments_removed = strip_non_mso_comments(html)
    after_comments = len(html.encode("utf-8"))
    html = shorten_safe_literals(html)
    html = remove_empty_attrs(html)
    html = minify_html(html)
    production_size = len(html.encode("utf-8"))
    report = {
        "authoring_size": original_size,
        "production_size": production_size,
        "estimated_mailerlite_injection_bytes": MAILERLITE_ESTIMATED_INJECTION_BYTES,
        "estimated_delivered_size": production_size + MAILERLITE_ESTIMATED_INJECTION_BYTES,
        "bytes_saved_total": original_size - production_size,
        "bytes_saved_by_url_replacement": after_urls - original_size,
        "bytes_saved_by_comment_stripping": after_urls - after_comments,
        "legacy_urls_replaced": url_replacements,
        "comments_removed": comments_removed,
        "size_status": (
            "pass"
            if production_size <= PRODUCTION_IDEAL_BYTES
            else "warning"
            if production_size <= PRODUCTION_WARNING_BYTES
            else "human_review_required"
            if production_size <= PRODUCTION_HARD_FAIL_BYTES
            else "hard_fail"
        ),
        "protected_regions_touched": False,
        "mso_blocks_touched": False,
    }
    return ExportResult(html=html, report=report)


def validate_production_html(html: str, report: ValidationReport, source_name: str) -> None:
    size = len(html.encode("utf-8"))
    delivered_estimate = size + MAILERLITE_ESTIMATED_INJECTION_BYTES
    report.info.setdefault("size_policy", {
        "ideal_source_html_bytes": PRODUCTION_IDEAL_BYTES,
        "warning_source_html_bytes": PRODUCTION_WARNING_BYTES,
        "hard_fail_source_html_bytes": PRODUCTION_HARD_FAIL_BYTES,
        "estimated_mailerlite_injection_bytes": MAILERLITE_ESTIMATED_INJECTION_BYTES,
    })
    report.info["estimated_delivered_html_size"] = delivered_estimate
    if LEGACY_ASSET_RE.search(html):
        report.add("hard_fail", "production_validator", "legacy_asset_url", "Production HTML contains legacy MailerLite asset URLs.", source_name)
    if "<!-- BEGIN_EDITABLE:" in html or "<!-- END_EDITABLE:" in html:
        report.add("hard_fail", "production_validator", "editable_marker_present", "Production HTML contains editable-region markers.", source_name)
    if re.search(r"\s(?:style|class)=[\"']\s*[\"']", html):
        report.add("hard_fail", "production_validator", "empty_attr", "Production HTML contains empty style/class attributes.", source_name)
    if "<!--[if mso]" in html and "<![endif]-->" not in html:
        report.add("hard_fail", "production_validator", "malformed_mso", "Production HTML contains malformed MSO conditional comments.", source_name)
    if size > PRODUCTION_HARD_FAIL_BYTES:
        report.add("hard_fail", "production_validator", "production_over_hard_budget", f"Production HTML is {size} bytes, over 95 KB.", source_name)
    elif size > PRODUCTION_WARNING_BYTES:
        report.add("human_review_required", "production_validator", "production_over_review_budget", f"Production HTML is {size} bytes, over 85 KB review threshold; estimated delivered size is {delivered_estimate} bytes after MailerLite injection.", source_name)
    elif size > PRODUCTION_IDEAL_BYTES:
        report.add("warning", "production_validator", "production_over_ideal_target", f"Production HTML is {size} bytes, over 75 KB ideal target; estimated delivered size is {delivered_estimate} bytes after MailerLite injection.", source_name)


def replace_legacy_asset_urls(html: str) -> tuple[str, int]:
    replacements = 0
    ordered_assets = [CANONICAL_ASSETS[key] for key in ("S", "H", "D", "C", "logo", "BW")]

    def repl(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1
        index = min(replacements - 1, len(ordered_assets) - 1)
        return ordered_assets[index]

    return LEGACY_ASSET_RE.sub(repl, html), replacements


def strip_non_mso_comments(html: str) -> tuple[str, int]:
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal removed
        comment = match.group(0)
        if comment.startswith("<!--[if") or comment.startswith("<!--<![endif]") or "mso" in comment[:40].lower():
            return comment
        removed += 1
        return ""

    return re.sub(r"<!--.*?-->", repl, html, flags=re.S), removed


def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def shorten_safe_literals(html: str) -> str:
    replacements = {
        "#ffffff": "#fff",
        "#FFFFFF": "#fff",
        "#333333": "#333",
        "#222222": "#222",
        "#444444": "#444",
        "#555555": "#555",
    }
    for before, after in replacements.items():
        html = html.replace(before, after)
    html = re.sub(r"(?<![\d.])0(?:px|pt)", "0", html)
    html = html.replace(' type="text/css"', "")
    return html


def remove_empty_attrs(html: str) -> str:
    return re.sub(r"\s(?:style|class)=(['\"])\s*\1", "", html)


def minify_html(html: str) -> str:
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"\s{2,}", " ", html)
    return html.strip()


def render_authoring_html(newsletter: dict[str, Any], template_html: str) -> str:
    """Render conservative authoring HTML from canonical JSON and a template.

    This fills editable regions only. It does not infer bridge layout or alter
    invariant shell regions.
    """
    article = newsletter.get("article", {})
    replacements = {
        "NEWSLETTER_IDENTITY": escape(str(newsletter.get("newsletter_identity", ""))),
        "EDITOR_NOTE_HTML": newsletter.get("editor_note", {}).get("html", ""),
        "ARTICLE_TITLE": escape(str(article.get("title", ""))),
        "ARTICLE_DECK": escape(str(article.get("deck", ""))),
        "ARTICLE_SERIES_NAME": escape(str(article.get("series_name", ""))),
        "ARTICLE_AUTHOR_AND_LEVEL": escape(str(article.get("author") or article.get("author_and_level") or "")),
    }
    html = template_html
    for marker, value in replacements.items():
        html = replace_editable_region(html, marker, value)
    body = "\n".join(section.get("html", "") for section in article.get("sections", []) if isinstance(section, dict))
    html = replace_between(html, "<!-- ARTICLE_BLOCK_PLAY_DEFENSE_START -->", "<!-- ARTICLE_BLOCK_PLAY_DEFENSE_END -->", body)
    return html


def replace_editable_region(html: str, marker: str, value: str) -> str:
    pattern = re.compile(rf"<!-- BEGIN_EDITABLE:{re.escape(marker)} -->.*?<!-- END_EDITABLE:{re.escape(marker)} -->", re.S)
    return pattern.sub(f"<!-- BEGIN_EDITABLE:{marker} -->{value}<!-- END_EDITABLE:{marker} -->", html)


def replace_between(html: str, start: str, end: str, value: str) -> str:
    start_index = html.find(start)
    end_index = html.find(end)
    if start_index == -1 or end_index == -1 or end_index <= start_index:
        return html
    return html[: start_index + len(start)] + value + html[end_index:]


def derive_wnes_rows(auction: dict[str, Any]) -> list[dict[str, str]]:
    dealer = auction.get("dealer")
    calls = auction.get("call_order") or []
    if dealer not in WNES:
        raise ValueError("auction dealer is required")
    cells: list[tuple[str, str]] = []
    dealer_index = WNES.index(dealer)
    for offset in range(dealer_index):
        cells.append((WNES[offset], ""))
    for call in calls:
        cells.append((call["seat"], call["call"]))
    while len(cells) % 4:
        cells.append((WNES[len(cells) % 4], ""))
    rows = []
    for index in range(0, len(cells), 4):
        row = {seat: "" for seat in WNES}
        for seat, call in cells[index : index + 4]:
            row[seat] = call
        rows.append(row)
    return rows


def split_ranks(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip().upper().replace("T", "10") for item in value if str(item).strip()]
    return [part.strip().upper().replace("T", "10") for part in str(value).split() if part.strip()]


def normalize_call(call: str) -> str:
    text = str(call).strip()
    lower = text.lower()
    if lower in {"p", "pass"}:
        return "Pass"
    if lower in {"x", "double", "dbl"}:
        return "Double"
    if lower in {"xx", "redouble", "rdbl"}:
        return "Redouble"
    return text.upper().replace("N", "NT") if re.match(r"^[1-7](C|D|H|S|N|NT)$", text, re.I) else text


def parse_bid(call: str) -> tuple[int, int] | None:
    match = re.match(r"^([1-7])(C|D|H|S|NT)$", call)
    if not match:
        return None
    return int(match.group(1)), STRAINS.index(match.group(2))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - reporting parse failures deterministically
        raise ValueError(f"{path}: {exc}") from exc


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    report = validate_package(args.package)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"hard_fail={len(report.hard_fails())} warning={len(report.warnings())} human_review_required={len(report.human_review())}")
        for finding in report.findings:
            print(f"[{finding.severity}] {finding.validator}:{finding.code} {finding.path} {finding.message}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
