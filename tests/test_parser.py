from packages.aims_parser import parse_dxf


def test_parse_simple_site():
    adf = parse_dxf("examples/simple_site.dxf")
    assert adf.feature_count >= 2
    assert "CAD_BOUNDARY" in adf.layers
