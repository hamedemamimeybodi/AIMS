from packages.aims_core.adf import ADFDocument, ADFEntity, ADFCategory, ADFGeometry
from packages.aims_openbim.openbim_validation import validate_openbim


def test_openbim_validation_assigns_guid_and_flags_missing_pset():
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-WALL",
                category=ADFCategory.WALL,
                bim_class="IfcWall",
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [1, 0], [1, 1]]),
                properties={"level": "Ground Floor"},
            )
        ],
    )
    standard = {"openbim": {"required_pset_properties": {"IfcWall": ["level", "material"]}}}
    report = validate_openbim(doc, standard=standard)
    assert report.openbim_entities == 1
    assert report.missing_ifc_guid == 1
    assert report.missing_pset_properties == 1
    assert doc.entities[0].properties["ifc_guid"] == doc.entities[0].id
    assert any(issue.code == "OPENBIM_GUID_ASSIGNED" for issue in doc.entities[0].issues)
    assert any(issue.code == "OPENBIM_MISSING_PSET_PROPERTY" for issue in doc.entities[0].issues)


def test_openbim_validation_counts_unsupported_ifc_class():
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[ADFEntity(entity_type="3DSOLID", layer="A-MASS", category=ADFCategory.UNKNOWN, bim_class="IfcBuildingElementProxy")],
    )
    report = validate_openbim(doc)
    assert report.unsupported_ifc_classes == 1
    assert report.openbim_entities == 0
    assert report.score <= 70
