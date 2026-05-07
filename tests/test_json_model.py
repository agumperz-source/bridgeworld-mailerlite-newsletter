import json
from pathlib import Path

from tbw_converter.validation_core import validate_newsletter_json


def test_defense_fixture_is_schema_valid():
    fixture = json.loads(Path("fixtures/defense_problem.expected.json").read_text(encoding="utf-8"))

    report = validate_newsletter_json(fixture, "defense_problem.expected.json")

    assert not report.hard_fails()
