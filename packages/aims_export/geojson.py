from __future__ import annotations

import json

from packages.aims_domain import ADFDocument


def to_geojson(adf: ADFDocument) -> str:
    features = []
    for f in adf.features:
        features.append({
            "type": "Feature",
            "id": f.feature_id,
            "properties": {
                "layer": f.layer,
                "source_entity": f.source_entity,
                **f.attributes,
            },
            "geometry": {
                "type": f.geometry.type,
                "coordinates": f.geometry.coordinates,
            },
        })
    return json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2)
