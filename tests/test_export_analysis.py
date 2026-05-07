from pathlib import Path

from tbw_converter.export_analysis import analyze_file, analyze_html_size


def test_export_analysis_counts_repeated_styles():
    html = '<table style="font-size:17px"><tr><td style="font-size:17px">X</td></tr></table>'

    report = analyze_html_size(html)

    assert report["total_bytes"] == len(html.encode("utf-8"))
    assert report["top_repeated_style_attributes"][0]["count"] == 2


def test_production_template_analysis_has_size_buckets():
    report = analyze_file(Path("templates/production_canonical.html"))
    bucket_names = {bucket["name"] for bucket in report["buckets"]}

    assert "style_attributes" in bucket_names
    assert "mso_blocks" in bucket_names
    assert report["total_bytes"] > 75_000
