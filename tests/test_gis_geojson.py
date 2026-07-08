from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity, ADFGeometry
from packages.aims_gis.geojson_export import document_to_feature_collection


def test_closed_polyline_exports_as_polygon():
    doc = ADFDocument(
        source_file="sample.dxf",
        entities=[
            ADFEntity(
                entity_type="LWPOLYLINE",
                layer="A-ROOM",
                category=ADFCategory.ROOM,
                geometry=ADFGeometry(type="polyline", closed=True, points=[[0, 0], [2, 0], [2, 2], [0, 2]]),
            )
        ],
    )
    fc = document_to_feature_collection(doc)
    assert fc["type"] == "FeatureCollection"
    assert len(fc["features"]) == 1
    assert fc["features"][0]["geometry"]["type"] == "Polygon"
    assert fc["features"][0]["geometry"]["coordinates"][0][0] == [0.0, 0.0]
