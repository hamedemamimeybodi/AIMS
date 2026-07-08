from packages.aims_bim.bim_mapping import apply_bim_mapping
from packages.aims_bim.readiness import compute_bim_readiness
from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity


def test_bim_readiness_flags_missing_level_and_material():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[ADFEntity(entity_type="LWPOLYLINE", layer="A-WALL", category=ADFCategory.WALL)],
    )
    apply_bim_mapping(doc)

    report = compute_bim_readiness(doc)

    assert report.bim_entities == 1
    assert report.missing_level == 1
    assert report.missing_material == 1
    assert any(i.code == "BIM_MISSING_LEVEL" for i in doc.entities[0].issues)
    assert any(i.code == "BIM_MISSING_MATERIAL" for i in doc.entities[0].issues)


def test_bim_readiness_accepts_complete_properties():
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

    report = compute_bim_readiness(doc)

    assert report.missing_level == 0
    assert report.missing_material == 0
    assert report.score == 100
