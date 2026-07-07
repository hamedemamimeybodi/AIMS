from packages.aims_parser import parse_dxf
from packages.aims_validator import validate_document


def test_validation_runs():
    adf = parse_dxf("examples/simple_site.dxf")
    report = validate_document(adf)
    assert report.error_count == 0
