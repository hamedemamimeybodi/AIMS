from packages.aims_parser import parse_dxf
from packages.aims_report import to_markdown
from packages.aims_validator import validate_document


def test_markdown_report_contains_title():
    adf = parse_dxf("examples/simple_site.dxf")
    report = validate_document(adf)
    md = to_markdown(adf, report)
    assert "AIMS Validation Report" in md
