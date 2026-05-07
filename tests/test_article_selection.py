from tbw_converter.extract_pdf import build_source_inventory, extract_pdf, ExtractionUnavailable


def test_source_inventory_is_fail_closed_unknown():
    inventory = build_source_inventory(["source.pdf"])

    assert inventory[0].classification == "unknown"
    assert inventory[0].status == "human_review_required"


def test_pdf_extraction_fails_rather_than_guessing():
    try:
        extract_pdf("source.pdf")
    except ExtractionUnavailable as exc:
        assert "fail rather than infer" in str(exc)
    else:
        raise AssertionError("extract_pdf must fail closed until raster/OCR is implemented")
