from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_rules.engine import apply_rule_engine


def test_rule_engine_flags_open_room_boundary():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", points=[[0, 0], [1, 0], [1, 1]], closed=False),
            )
        ],
    )
    standard = {
        "rule_sets": {
            "test": {
                "rules": [
                    {
                        "id": "ROOM_REQUIRES_CLOSED_BOUNDARY",
                        "selector": {"category": "Room"},
                        "severity": "error",
                        "message": "Room must be closed.",
                        "conditions": [{"op": "closed_geometry"}],
                    }
                ]
            }
        }
    }

    result = apply_rule_engine(doc, standard)

    assert result.total_rules == 1
    assert result.failed == 1
    assert result.score == 0
    assert doc.entities[0].issues[0].code == "ROOM_REQUIRES_CLOSED_BOUNDARY"
    assert doc.entities[0].issues[0].severity == "error"


def test_rule_engine_passes_complete_bim_relevant_entity():
    doc = ADFDocument(
        source_file="unit-test.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-WALL",
                category=ADFCategory.WALL,
                bim_class="IfcWall",
                properties={"level": "Ground Floor"},
                geometry=ADFGeometry(type="polyline", points=[[0, 0], [3, 0]], closed=False),
            )
        ],
    )
    standard = {
        "entity_rules": [
            {
                "id": "BIM_RELEVANT_REQUIRES_LEVEL",
                "selector": {"category": "Wall"},
                "severity": "warning",
                "message": "Level required.",
                "conditions": [{"op": "not_empty", "field": "level"}],
            },
            {
                "id": "BIM_RELEVANT_REQUIRES_IFC_CLASS",
                "selector": {"category": "Wall"},
                "severity": "warning",
                "message": "IFC class required.",
                "conditions": [{"op": "exists", "field": "bim_class"}],
            },
        ]
    }

    result = apply_rule_engine(doc, standard)

    assert result.failed == 0
    assert result.passed == 2
    assert result.score == 100
    assert doc.entities[0].issues == []
