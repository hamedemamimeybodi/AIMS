from pathlib import Path

from packages.aims_bim.bim_mapping import apply_bim_mapping
from packages.aims_bim.readiness import compute_bim_readiness
from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity
from packages.aims_report.markdown_report import write_markdown_report


def test_report_contains_bim_readiness(tmp_path: Path):
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-WALL",
                category=ADFCategory.WALL,
                properties={"level": "Ground Floor", "material": "Concrete"},
            )
        ],
    )
    apply_bim_mapping(doc)
    bim = compute_bim_readiness(doc)

    out = tmp_path / "report.md"
    write_markdown_report(doc, out, bim_readiness=bim)

    content = out.read_text(encoding="utf-8")
    assert "BIM readiness score" in content
    assert "IfcWall" in content
