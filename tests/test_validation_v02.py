from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_geometry.validation import validate_document


def test_duplicate_geometry_is_detected():
    doc = ADFDocument(source_file="x.dxf")
    geom = ADFGeometry(type="line", points=[[0, 0, 0], [1, 0, 0]])
    doc.entities.append(ADFEntity(entity_type="LINE", layer="A-WALL", category=ADFCategory.WALL, geometry=geom))
    doc.entities.append(ADFEntity(entity_type="LINE", layer="A-WALL", category=ADFCategory.WALL, geometry=geom))
    validate_document(doc, {"layers": {"A-WALL": {"category": "Wall"}}})
    assert any(issue.code == "DUPLICATE_GEOMETRY" for issue in doc.entities[0].issues)


def test_room_area_is_calculated():
    doc = ADFDocument(source_file="x.dxf")
    doc.entities.append(
        ADFEntity(
            entity_type="LWPOLYLINE",
            layer="A-ROOM",
            category=ADFCategory.ROOM,
            geometry=ADFGeometry(type="polyline", points=[[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]], closed=True),
        )
    )
    validate_document(doc, {"layers": {"A-ROOM": {"category": "Room"}}, "rules": {"min_room_area": 0.5}})
    assert doc.entities[0].properties["area"] == 4.0
