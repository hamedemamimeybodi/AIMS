from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_gis.topology import analyze_topology


def test_topology_detects_bbox_overlap():
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [2, 0], [2, 2], [0, 2]]),
            ),
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", closed=True, points=[[1, 1], [3, 1], [3, 3], [1, 3]]),
            ),
        ],
    )
    report = analyze_topology(doc)
    assert report.polygon_count == 2
    assert report.overlap_pair_count == 1
