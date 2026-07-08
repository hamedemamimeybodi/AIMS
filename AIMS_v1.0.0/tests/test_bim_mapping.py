from packages.aims_bim.bim_mapping import apply_bim_mapping
from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity


def test_apply_bim_mapping_by_category():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[ADFEntity(entity_type="LWPOLYLINE", layer="A-WALL", category=ADFCategory.WALL)],
    )

    result = apply_bim_mapping(doc)

    assert result.mapped_entities == 1
    assert result.unmapped_entities == 0
    assert doc.entities[0].bim_class == "IfcWall"
    assert doc.entities[0].properties["ifc_class"] == "IfcWall"


def test_apply_bim_mapping_by_block_override():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="INSERT",
                layer="A-DOOR",
                category=ADFCategory.UNKNOWN,
                properties={"block_name": "DOOR-SINGLE"},
            )
        ],
    )
    standard = {"bim": {"ifc_by_block": {"DOOR-SINGLE": "IfcDoor"}}}

    result = apply_bim_mapping(doc, standard=standard)

    assert result.mapped_entities == 1
    assert doc.entities[0].bim_class == "IfcDoor"
