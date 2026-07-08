from pathlib import Path

from packages.aims_parser.dxf_parser import _parse_dxf_fallback


def test_fallback_parser_reads_simple_site():
    root = Path(__file__).resolve().parents[1]
    doc = _parse_dxf_fallback(root / "examples" / "simple_site.dxf")
    assert len(doc.entities) == 5
    assert {entity.entity_type for entity in doc.entities} >= {"LWPOLYLINE", "LINE", "TEXT", "INSERT"}
