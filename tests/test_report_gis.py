from pathlib import Path

from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_gis.readiness import compute_gis_readiness
from packages.aims_report.markdown_report import write_markdown_report


def test_markdown_report_contains_gis_section(tmp_path: Path):
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                properties={"level": "Ground Floor"},
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [2, 0], [2, 2], [0, 2]]),
            )
        ],
    )
    gis = compute_gis_readiness(doc)
    out = write_markdown_report(doc, tmp_path / "report.md", gis_readiness=gis)
    text = out.read_text(encoding="utf-8")
    assert "## GIS Readiness" in text
    assert "GIS readiness score" in text
