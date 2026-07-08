from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from packages.aims_core.adf import ADFDocument, ADFEntity


def _coords_2d(points: list[list[float]]) -> list[list[float]]:
    return [[float(p[0]), float(p[1])] for p in points]


def _geometry_to_geojson(entity: ADFEntity) -> Dict[str, Any] | None:
    if not entity.geometry or not entity.geometry.points:
        return None

    points = _coords_2d(entity.geometry.points)
    gtype = entity.geometry.type.lower()

    if gtype == "line":
        return {"type": "LineString", "coordinates": points}

    if gtype == "point":
        return {"type": "Point", "coordinates": points[0]}

    if gtype == "polyline":
        if entity.geometry.closed and len(points) >= 3:
            ring = points[:]
            if ring[0] != ring[-1]:
                ring.append(ring[0])
            return {"type": "Polygon", "coordinates": [ring]}
        return {"type": "LineString", "coordinates": points}

    return None


def entity_to_feature(entity: ADFEntity) -> Dict[str, Any] | None:
    geometry = _geometry_to_geojson(entity)
    if geometry is None:
        return None

    properties: Dict[str, Any] = {
        "id": entity.id,
        "source": entity.source,
        "handle": entity.handle,
        "entity_type": entity.entity_type,
        "layer": entity.layer,
        "category": entity.category.value,
        "bim_class": entity.bim_class,
        "text": entity.text,
        **entity.properties,
        "issue_codes": [issue.code for issue in entity.issues],
        "issue_count": len(entity.issues),
    }
    return {"type": "Feature", "geometry": geometry, "properties": properties}


def document_to_feature_collection(document: ADFDocument) -> Dict[str, Any]:
    features: List[Dict[str, Any]] = []
    for entity in document.entities:
        feature = entity_to_feature(entity)
        if feature:
            features.append(feature)
    return {
        "type": "FeatureCollection",
        "name": Path(document.source_file).stem or "aims_export",
        "features": features,
    }


def write_geojson(document: ADFDocument, out_path: str | Path) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    collection = document_to_feature_collection(document)
    out_path.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path
