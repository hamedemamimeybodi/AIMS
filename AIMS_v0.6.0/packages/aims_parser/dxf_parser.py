from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import ezdxf

from packages.aims_core.adf import ADFDocument, ADFEntity, ADFGeometry
from packages.aims_core.classification import bim_class_for, classify_layer


def _points_from_line(entity: Any) -> List[List[float]]:
    start = entity.dxf.start
    end = entity.dxf.end
    return [[float(start.x), float(start.y), float(getattr(start, "z", 0.0))], [float(end.x), float(end.y), float(getattr(end, "z", 0.0))]]


def _points_from_lwpolyline(entity: Any) -> List[List[float]]:
    points: List[List[float]] = []
    for p in entity.get_points("xy"):
        points.append([float(p[0]), float(p[1]), 0.0])
    return points


def _points_from_polyline(entity: Any) -> List[List[float]]:
    points: List[List[float]] = []
    for vertex in entity.vertices:
        loc = vertex.dxf.location
        points.append([float(loc.x), float(loc.y), float(getattr(loc, "z", 0.0))])
    return points


def _entity_to_adf(entity: Any, standard: Optional[Dict[str, Any]] = None) -> Optional[ADFEntity]:
    etype = entity.dxftype()
    layer = getattr(entity.dxf, "layer", "0")
    category = classify_layer(layer, standard)
    bim_class = bim_class_for(category, layer_name=layer, standard=standard)
    handle = getattr(entity.dxf, "handle", None)

    if etype == "LINE":
        geometry = ADFGeometry(type="line", points=_points_from_line(entity), closed=False)
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=geometry)

    if etype == "LWPOLYLINE":
        points = _points_from_lwpolyline(entity)
        geometry = ADFGeometry(type="polyline", points=points, closed=bool(entity.closed))
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=geometry)

    if etype == "POLYLINE":
        points = _points_from_polyline(entity)
        geometry = ADFGeometry(type="polyline", points=points, closed=bool(entity.is_closed))
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=geometry)

    if etype in {"TEXT", "MTEXT"}:
        text = entity.plain_text() if etype == "MTEXT" else str(entity.dxf.text)
        insert = getattr(entity.dxf, "insert", None)
        points = [] if insert is None else [[float(insert.x), float(insert.y), float(getattr(insert, "z", 0.0))]]
        geometry = ADFGeometry(type="point", points=points, closed=False)
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=geometry, text=text)

    if etype == "INSERT":
        name = str(entity.dxf.name)
        insert = entity.dxf.insert
        geometry = ADFGeometry(type="block_insert", points=[[float(insert.x), float(insert.y), float(getattr(insert, "z", 0.0))]], raw={"block_name": name})
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=geometry, properties={"block_name": name})

    return None


def parse_dxf(path: str | Path, standard: Optional[Dict[str, Any]] = None) -> ADFDocument:
    path = Path(path)
    doc = ezdxf.readfile(path)
    modelspace = doc.modelspace()
    adf = ADFDocument(source_file=str(path), units=str(doc.header.get("$INSUNITS", "unknown")))

    for entity in modelspace:
        converted = _entity_to_adf(entity, standard=standard)
        if converted is not None:
            adf.entities.append(converted)

    return adf
