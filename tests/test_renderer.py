from tbw_converter.validation_core import export_production_html, derive_wnes_rows


def test_production_export_is_idempotent():
    authoring = '<html><!-- NOTE --><body><p style="">X</p></body></html>'

    first = export_production_html(authoring).html
    second = export_production_html(first).html

    assert first == second
    assert "<!-- NOTE -->" not in first
    assert 'style=""' not in first


def test_auction_derives_wnes_with_dealer_offset():
    rows = derive_wnes_rows(
        {
            "dealer": "N",
            "call_order": [
                {"seat": "N", "call": "1H"},
                {"seat": "E", "call": "Pass"},
                {"seat": "S", "call": "?"},
            ],
        }
    )

    assert rows[0] == {"W": "", "N": "1H", "E": "Pass", "S": "?"}
