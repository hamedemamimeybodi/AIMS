from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:  # pragma: no cover - exercised when ezdxf is installed
    import ezdxf  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback is covered in tests/CLI smoke
    ezdxf = None

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


def _pairs(lines: Iterable[str]) -> List[Tuple[str, str]]:
    cleaned = [line.rstrip("\n\r") for line in lines]
    return [(cleaned[i].strip(), cleaned[i + 1].strip()) for i in range(0, len(cleaned) - 1, 2)]


def _entity_records(pairs: List[Tuple[str, str]]) -> List[Dict[str, List[str]]]:
    in_entities = False
    current: Dict[str, List[str]] | None = None
    records: List[Dict[str, List[str]]] = []
    i = 0
    while i < len(pairs):
        code, value = pairs[i]
        if code == "0" and value == "SECTION" and i + 1 < len(pairs) and pairs[i + 1] == ("2", "ENTITIES"):
            in_entities = True
            i += 2
            continue
        if in_entities and code == "0" and value == "ENDSEC":
            if current:
                records.append(current)
            break
        if in_entities and code == "0":
            if current:
                records.append(current)
            current = {"0": [value]}
        elif in_entities and current is not None:
            current.setdefault(code, []).append(value)
        i += 1
    return records


def _float_at(values: List[str], idx: int, default: float = 0.0) -> float:
    try:
        return float(values[idx])
    except (IndexError, TypeError, ValueError):
        return default


def _fallback_record_to_adf(record: Dict[str, List[str]], standard: Optional[Dict[str, Any]] = None) -> Optional[ADFEntity]:
    etype = record.get("0", [""])[0]
    layer = record.get("8", ["0"])[0]
    handle = record.get("5", [None])[0]
    category = classify_layer(layer, standard)
    bim_class = bim_class_for(category, layer_name=layer, standard=standard)

    if etype == "LINE":
        points = [[_float_at(record.get("10", []), 0), _float_at(record.get("20", []), 0), _float_at(record.get("30", []), 0)], [_float_at(record.get("11", []), 0), _float_at(record.get("21", []), 0), _float_at(record.get("31", []), 0)]]
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=ADFGeometry(type="line", points=points, closed=False))

    if etype == "LWPOLYLINE":
        xs = record.get("10", [])
        ys = record.get("20", [])
        points = [[float(x), float(ys[idx] if idx < len(ys) else 0.0), 0.0] for idx, x in enumerate(xs)]
        flags = int(float(record.get("70", ["0"])[0])) if record.get("70") else 0
        closed = bool(flags & 1)
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=ADFGeometry(type="polyline", points=points, closed=closed))

    if etype == "TEXT":
        points = [[_float_at(record.get("10", []), 0), _float_at(record.get("20", []), 0), _float_at(record.get("30", []), 0)]]
        text = record.get("1", [""])[0]
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=ADFGeometry(type="point", points=points), text=text)

    if etype == "INSERT":
        name = record.get("2", [""])[0]
        points = [[_float_at(record.get("10", []), 0), _float_at(record.get("20", []), 0), _float_at(record.get("30", []), 0)]]
        return ADFEntity(handle=handle, entity_type=etype, layer=layer, category=category, bim_class=bim_class, geometry=ADFGeometry(type="block_insert", points=points, raw={"block_name": name}), properties={"block_name": name})

    return None


def _parse_dxf_fallback(path: Path, standard: Optional[Dict[str, Any]] = None) -> ADFDocument:
    pairs = _pairs(path.read_text(encoding="utf-8", errors="ignore").splitlines())
    adf = ADFDocument(source_file=str(path), units="fallback")
    for record in _entity_records(pairs):
        converted = _fallback_record_to_adf(record, standard=standard)
        if converted is not None:
            adf.entities.append(converted)
    return adf


def parse_dxf(path: str | Path, standard: Optional[Dict[str, Any]] = None) -> ADFDocument:
    path = Path(path)
    if ezdxf is None:
        return _parse_dxf_fallback(path, standard=standard)

    doc = ezdxf.readfile(path)
    modelspace = doc.modelspace()
    adf = ADFDocument(source_file=str(path), units=str(doc.header.get("$INSUNITS", "unknown")))

    for entity in modelspace:
        converted = _entity_to_adf(entity, standard=standard)
        if converted is not None:
            adf.entities.append(converted)

    return adf
