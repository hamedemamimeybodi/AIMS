from pathlib import Path

from packages.aims_core.adf import ADFDocument, ADFEntity, ADFCategory, ADFGeometry
from packages.aims_openbim.ifc_export import export_ifc_text, write_ifc


def _doc():
    return ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                id="wall-1",
                entity_type="LWPOLYLINE",
                layer="A-WALL",
                category=ADFCategory.WALL,
                bim_class="IfcWall",
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [2, 0], [2, 1]]),
                properties={"level": "L1", "material": "Concrete", "ifc_guid": "GUID-WALL-1"},
            ),
            ADFEntity(entity_type="LINE", layer="0", category=ADFCategory.UNKNOWN),
        ],
    )


def test_export_ifc_text_contains_project_and_entity():
    text, result = export_ifc_text(_doc(), standard={"openbim": {"project_name": "Demo"}})
    assert "ISO-10303-21" in text
    assert "IFCPROJECT" in text
    assert "IfcWall" in text
    assert "GUID-WALL-1" in text
    assert result.exportable_entities == 1
    assert result.skipped_entities == 1
    assert result.ifc_class_counts["IfcWall"] == 1


def test_write_ifc_creates_file(tmp_path: Path):
    out = tmp_path / "model.ifc"
    result = write_ifc(_doc(), out)
    assert out.exists()
    assert result.output_path == str(out)
    assert "IfcWall" in out.read_text(encoding="utf-8")
