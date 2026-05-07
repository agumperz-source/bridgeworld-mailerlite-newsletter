from pathlib import Path

from tbw_converter.fingerprints import fingerprint_file, validate_protected_fingerprints


def test_production_template_has_protected_fingerprints():
    html = Path("templates/production_canonical.html").read_text(encoding="utf-8-sig")

    errors = validate_protected_fingerprints(html)

    assert errors == []


def test_protected_fingerprint_report_contains_named_regions():
    report = fingerprint_file("templates/production_canonical.html")
    names = {region["name"] for region in report["regions"]}

    assert "newsletter_identity" in names
    assert "mso_auction" in names
    assert "footer" in names
