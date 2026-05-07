from tbw_converter.validation_core import (
    ValidationReport,
    validate_html_component_guardrails,
)


def collect_codes(html: str) -> set[str]:
    report = ValidationReport()
    validate_html_component_guardrails(html, report, "sample.html")
    return {finding.code for finding in report.findings}


def test_auction_footnote_inside_table_is_rejected():
    html = """
    <table class="tbw-auction-table">
      <tr><td>WEST</td><td>NORTH</td><td>EAST</td><td>SOUTH</td></tr>
      <tr><td>1 NT*</td><td>Pass</td><td>2 C**</td><td>Pass</td></tr>
      <tr><td colspan="4">* 10-12<br>** both majors</td></tr>
    </table>
    """

    assert "auction_footnote_inside_table" in collect_codes(html)


def test_nested_footer_shell_is_rejected():
    html = """
    <table><tr><td>Article body</td></tr></table>
    <table><tr><td>Stay Connected
      <table width="600"><tr><td>Nested shell</td></tr></table>
    </td></tr></table>
    """

    assert "nested_footer_shell" in collect_codes(html)


def test_unbalanced_table_tags_are_rejected():
    html = "<table><tr><td>Missing close</td></tr>"

    assert "unbalanced_table_tags" in collect_codes(html)


def test_dangerous_css_comment_is_warned():
    html = "<style>.x{color:#333}/* <span>comment</span> */</style>"

    assert "dangerous_css_comment" in collect_codes(html)
