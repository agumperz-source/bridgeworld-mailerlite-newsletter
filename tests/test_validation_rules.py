import json
from pathlib import Path

from tbw_converter.validation_core import validate_newsletter_json


def test_duplicate_card_fixture_hard_fails():
    fixture = json.loads(Path("fixtures/duplicate_card.hard_fail.json").read_text(encoding="utf-8"))

    report = validate_newsletter_json(fixture, "duplicate_card.hard_fail.json")

    assert any(item.code == "duplicate_card" for item in report.hard_fails())
