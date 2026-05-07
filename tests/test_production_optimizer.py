from pathlib import Path

from tbw_converter.production_optimizer import optimize_production_html


def test_style_block_optimizer_saves_bytes_without_changing_body_markup():
    html = "<style>/* note */ .x { color : #fff ; }</style><body><table><tr><td>X</td></tr></table></body>"

    result = optimize_production_html(html)

    assert result.report["bytes_saved"] > 0
    assert "<body><table><tr><td>X</td></tr></table></body>" in result.html


def test_production_template_css_optimizer_is_idempotent_after_application():
    html = Path("templates/production_canonical.html").read_text(encoding="utf-8-sig")

    result = optimize_production_html(html)

    assert result.report["bytes_saved"] == 0
    assert result.html == html
    assert result.report["protected_fingerprints_changed"] is False
