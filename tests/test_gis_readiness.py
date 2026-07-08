from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_gis.readiness import compute_gis_readiness


def test_gis_readiness_counts_exportable_features_and_missing_level():
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [3, 0], [3, 3], [0, 3]]),
            ),
            ADFEntity(entity_type="TEXT", layer="A-TEXT", category=ADFCategory.TEXT, text="Room"),
        ],
    )
    report = compute_gis_readiness(doc)
    assert report.total_entities == 2
    assert report.exportable_features == 1
    assert report.missing_geometry == 1
    assert report.missing_level == 1
    assert report.topology.polygon_count == 1
    assert report.score < 100
